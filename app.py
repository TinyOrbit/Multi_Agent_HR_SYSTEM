import os
import uuid
import json
import logging

import google.cloud.logging
from fastapi import FastAPI
from dotenv import load_dotenv
from google.genai import types
from google.adk.runners import Runner
from fastapi.responses import JSONResponse
from google.adk.sessions import InMemorySessionService



from src.schema import File_Inputs
from src.agents import root_agent




# --- 1. Environment Setup & Logging ---
load_dotenv()
cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



SESSION_FILE = "session_ids.json"



def load_or_create_session_ids():
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                data = json.load(f)
                logger.info("Loaded session IDs from file.")
                return data["USER_ID"], data["SESSION_ID_TOOL_AGENT"]
        except Exception as e:
            logger.warning(f"Failed to load session IDs, generating new ones. Error: {e}")
    # If file doesn't exist or fails to load, generate new IDs
    user_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())
    with open(SESSION_FILE, "w") as f:
        json.dump({"USER_ID": user_id, "SESSION_ID_TOOL_AGENT": session_id}, f)
    logger.info("Generated new session IDs and saved to file.")
    return user_id, session_id

# --- 2. Constants ---
APP_NAME = "HR_SYSTEM_AGENT"
USER_ID, SESSION_ID_TOOL_AGENT = load_or_create_session_ids()
MODEL_NAME = os.getenv("MODEL", "gemini-2.0-flash")

# --- 3. Session Management & Runner ---
session_service = InMemorySessionService()
agent_runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service
)

# --- 4. Utility Functions ---
def extract_json_from_code_block(text: str) -> str:
    """
    Extracts JSON string from a code block like ```json ... ```
    If no code block is found, returns the original text.
    """
    if not isinstance(text, str):
        return text
    return text.replace("```json", "").replace("```", "")

# --- 5. FastAPI App Setup ---
app = FastAPI(
    title="HR Resume Multi-Agent API",
    description="API for extracting, processing, and analyzing resumes using a multi-agent system powered by Google ADK. Supports file extraction, LinkedIn enrichment, and context saving in a robust, orchestrated workflow.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID_TOOL_AGENT
    )
    logger.info("Session created on startup.")

@app.post("/multi_agent_call", summary="Process resume using multi-agent workflow")
async def process_resume_multi_agent(request: File_Inputs):
    query_json = json.dumps(request.dict())
    result = {}

    async def run():
        user_content = types.Content(role='user', parts=[types.Part(text=query_json)])
        final_response_content = "No final response received."
        try:
            async for event in agent_runner.run_async(
                user_id=USER_ID,
                session_id=SESSION_ID_TOOL_AGENT,
                new_message=user_content
            ):
                if event.is_final_response() and event.content and event.content.parts:
                    final_response_content = event.content.parts[0].text
        except Exception as e:
            logger.exception("Error during agent run_async")
            raise RuntimeError(f"Agent execution failed: {e}")
        return final_response_content

    try:
        response = await run()
        logger.info("Agent run completed.")

        # Get session state
        try:
            current_session = await session_service.get_session(
                app_name=APP_NAME,
                user_id=USER_ID,
                session_id=SESSION_ID_TOOL_AGENT
            )
            stored_output = current_session.state.get(root_agent.output_key)
            try:
                parsed_output = json.loads(stored_output)
                result["session_state"] = parsed_output
            except Exception:
                result["session_state"] = stored_output
            logger.info("Session state retrieved.")
        except Exception as e:
            logger.exception("Error retrieving session state")
            result["session_state"] = f"Session retrieval error: {e}"

        try:
            response2 = extract_json_from_code_block(response)
            safe_response2 = response2.replace('\\', '\\\\')
            response_json_str = json.dumps(json.loads(safe_response2), indent=4)
            result["response"] = response2
            response_1 = json.loads(response_json_str)
            logger.info("Agent response parsed successfully.")
            return JSONResponse(content={"response": response_1.get("save_context_to_json_response", {})})
        except Exception as e:
            logger.exception("Error parsing agent response")
            return JSONResponse(content={"error": f"Response parsing error: {e}"}, status_code=500)

    except Exception as e:
        logger.exception("Unhandled error in /multi_agent_call endpoint")
        return JSONResponse(content={"error": str(e)}, status_code=500)
