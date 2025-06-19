import os
import logging

from dotenv import load_dotenv
from google.adk import Agent
from google.adk.tools import FunctionTool
from google.adk.agents import SequentialAgent, LoopAgent, ParallelAgent, LlmAgent
from google.genai import types

from src.schema import File_Inputs, ResumeOutput
from src.tools import extract_text_from_file, fetch_linkedin_profile, save_context_to_json

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 1. Environment Setup ---
load_dotenv()
model_name = os.getenv("MODEL")
logger.info(f"Loaded model: {model_name}")

# --- 2. Tool Wrappers ---
save_context_tool = FunctionTool(func=save_context_to_json)
fetch_linkedin_tool = FunctionTool(func=fetch_linkedin_profile)
logger.info("Registered tools: save_context_tool, fetch_linkedin_tool")

# --- 3. Agent Definitions ---

extraction_agent = LlmAgent(
    name="file_path_data_extractor",
    description="Receives a file path to a resume (PDF or DOCX), uses the extract_text_from_file tool to extract all readable text from the file, and returns the raw extracted text exactly as found in the document, without any modification, inference, or reformatting. Handles unsupported file types with an appropriate error message.",
    instruction="""
    INSTRUCTIONS:
    You will receive a user profile file path in the variable called profile_path.
    Your task is to extract all readable text from the provided local file path (PDF, DOC, or DOCX).
    - Use the 'extract_text_from_file' tool to process the file.
    - Return the extracted text exactly as found in the document, without any modification, inference, or reformatting.
    - If the file type is unsupported, return an appropriate error message.
    """,
    generate_content_config=types.GenerateContentConfig(temperature=0),
    input_schema=File_Inputs,
    tools=[FunctionTool(func=extract_text_from_file)],
    output_key="extracted_text",
)
logger.info("Initialized extraction_agent")

formatter_agent = LlmAgent(
    name="extraction_formatter",
    model=model_name,
    description="Converts unstructured resume text into structured JSON data using the ResumeOutput Pydantic schema.",
    instruction="""
You will receive resume text in the variable {{extracted_text}}.
Your task:
- Carefully parse the provided resume text and extract all relevant information *exactly* as it appears in the text. Do not add, infer, or modify any information.
- Format the extracted information as a JSON object that strictly matches the ResumeOutput Pydantic schema. Ensure every field in the schema is present in the output. Use empty strings, empty lists, or None where data is missing in the extracted text.
- If the input text does not appear to be a valid resume, or if you are unable to extract any information, return an appropriate error message.
- Output a JSON object with fields: 'int_profile_data_json' contains all the fields of output schema.
""",
    generate_content_config=types.GenerateContentConfig(temperature=0),
    output_schema=ResumeOutput,
    output_key="int_profile_data_json",
)
logger.info("Initialized formatter_agent")

save_context_agent = LlmAgent(
    name="Context_Saver",
    model=model_name,
    description=(
        "Saves the extracted profile data to a JSON file with the name 'Profile_Analysis_Result_.json'. "
        "The file will contain the structured resume data extracted from the provided text. "
    ),
    instruction="""
You will receive resume text in the variable {{merged_context_json}}.
Take filename from profile_path context variable and save the merged context JSON data to a file named 'Profile_Analysis_Result_<filename>_YYYYMMDD_HHMMSS.json'.
For saving pass it to tool 'save_context_to_json' with the following parameters:
    - context_data: the merged JSON object
    - output_key: "Profile_Analysis_Result_json"
Ensure the file is saved in the current working directory.
and 
- The output from tool will be dictionary, just return the dictionary with as JSON
""",
    generate_content_config=types.GenerateContentConfig(temperature=0),
    tools=[save_context_tool],
    output_key="save_context",
)
logger.info("Initialized save_context_agent")

merge_context_agent = LlmAgent(
    name="merge_context_agent",
    model=model_name,
    description=(
        "Merges all available context variables (JSON outputs from previous agents) into a single JSON object. "
        "Each merged entry is assigned a key corresponding to its context variable name. "
        "The following context variables will be merged: "
        "{{int_profile_data_json}}, {{attribute_scores}}, {{semantic_match}}, {{final_ranking}}, {{enriched_profile_json}}, {{flagged_gaps_json}}, {{interview_questions_json}}."
    ),
    instruction="""
You will receive multiple context variables, each containing JSON data from previous agents:
- {{int_profile_data_json}}
- {{attribute_scores}}
- {{semantic_match}}
- {{final_ranking}}
- {{enriched_profile_json}}
- {{flagged_gaps_json}}
- {{interview_questions_json}}

Your task:
- For each context variable, assign its variable name as the key and its JSON content as the value.
- Merge all such key-value pairs into a single JSON object.
- Return the merged JSON object.
- If any context variable is missing or empty, skip it.
""",
    generate_content_config=types.GenerateContentConfig(temperature=0),
    output_key="merged_context_json",
)
logger.info("Initialized merge_context_agent")

profile_formation_agent = SequentialAgent(
    name="resume_extraction_pipeline",
    description="Extracts text in sequential manner",
    sub_agents=[extraction_agent, formatter_agent],
)
logger.info("Initialized profile_formation_agent")

jd_agent = LlmAgent(
    name="jd_parser",
    model=model_name,
    description="Parses the provided job description text and extracts structured requirements.",
    instruction="""
You will receive a job description in the variable job_description.
Your task:
- Carefully parse the job description and extract key requirements, skills, qualifications, and responsibilities *exactly* as they appear in the text. Do not add, infer, or modify any information.
- Format the extracted information as a JSON object.
- If the input is not a valid job description, or if you are unable to extract any information, return an appropriate error message.
""",
    generate_content_config=types.GenerateContentConfig(temperature=0),
    output_key="jd_json",
)
logger.info("Initialized jd_agent")

parallel_agent = ParallelAgent(
    name="resume_and_jd_parallel",
    description="Processes profile_path to profile_formation_agent and pass job_description key information to jd_agent in parallel.",
    sub_agents=[profile_formation_agent, jd_agent],
)
logger.info("Initialized parallel_agent")

match_agent = Agent(
    name="profile_jd_matcher",
    model=model_name,
    description="Compares structured resume data and job description to compute attribute match scores.",
    instruction="""
You will receive:
- Resume data in the variable {{int_profile_data_json}}
- Job description data in the variable {{jd_json}}

Your task:
- Compare the resume data and job description data.
- Compute and return a set of attribute scores (e.g., skill match, experience match, education match, overall fit).
- Output a JSON object with fields: 'attribute_scores' contains fields 'skill_match','experience_match','education_match','certification_match' and 'overall_fit' .
""",
    generate_content_config=types.GenerateContentConfig(temperature=0),
    output_key="attribute_scores",
)
logger.info("Initialized match_agent")

semantic_scoring_agent = Agent(
    name="semantic_scoring_agent",
    model=model_name,
    description="Performs semantic scoring and ranking of candidate profiles against job requirements using job-role ontologies.",
    instruction="""
You will receive:
- Resume data in the variable {{int_profile_data_json}}
- Job description data in the variable {{jd_json}}

Your task:
- Analyze the candidate's qualifications and experience against the job requirements and project needs.
- Use semantic similarity and job-role ontologies to assess the match between the candidate and the job.
- Rank the candidate and provide a semantic match score (0-100), along with a brief explanation for the score.
- Output a JSON object with fields: 'semantic_score', 'ranking', and 'explanation'.
""",
    generate_content_config=types.GenerateContentConfig(temperature=0),
    output_key="semantic_match",
)
logger.info("Initialized semantic_scoring_agent")

final_ranking_agent = Agent(
    name="final_ranking_agent",
    model=model_name,
    description="Aggregates attribute scores and semantic match to provide a final candidate ranking and summary.",
    instruction="""
You will receive:
- Attribute scores in the variable {{attribute_scores}}
- Semantic match in the variable {{semantic_match}}

Your task:
- Aggregate the attribute scores and semantic match score.
- Provide a final ranking, overall match percentage, and a summary explanation.
- Output a JSON object with fields: 'final_score', 'ranking', and 'summary'.
""",
    generate_content_config=types.GenerateContentConfig(temperature=0),
    output_key="final_ranking",
)
logger.info("Initialized final_ranking_agent")

external_hr_enrichment_agent = Agent(
    name="external_hr_enrichment_agent",
    model=model_name,
    description="Checks for LinkedIn profile URL in the candidate profile and fetches additional info if present. If LinkedIn URL is not found, returns a single line indicating this.",
    instruction="""
You will receive structured resume data in the variable {{int_profile_data_json}}.
Your task:
- If a LinkedIn profile URL is present, use the 'fetch_linkedin_profile' tool to fetch additional candidate information and output the enriched profile as JSON.
- If a LinkedIn profile URL is NOT present, return a JSON object with a single field: {"linkedin_profile": "not found"}.
- Do not prompt or return any other information if the LinkedIn URL is missing.
""",
    generate_content_config=types.GenerateContentConfig(temperature=0),
    tools=[fetch_linkedin_tool],
    output_key="enriched_profile_json"
)
logger.info("Initialized external_hr_enrichment_agent")

gap_flagging_agent = Agent(
    name="gap_flagging_agent",
    model=model_name,
    description="Flags mismatches or gaps in candidate profiles, such as expired certifications or missing skills, and displays the results in JSON format.",
    instruction="""
You will receive:
- Enriched candidate profile in the variable {{enriched_profile_json}}
- Job description data in the variable {{jd_json}}

Your task:
- Analyze the candidate profile for mismatches or gaps (e.g., expired certifications, missing or critical skills).
- Flag and list all issues found.
- Output a JSON object with a list of flagged issues and their details.
- Display the flagged gaps and issues in JSON format.
""",
    generate_content_config=types.GenerateContentConfig(temperature=0),
    output_key="flagged_gaps_json"
)
logger.info("Initialized gap_flagging_agent")

interview_question_agent = Agent(
    name="interview_question_agent",
    model=model_name,
    description="Suggests interview questions or skill assessments based on the job role and candidate profile.",
    instruction="""
You will receive:
- Enriched candidate profile in the variable {{enriched_profile_json}}
- Job description data in the variable {{jd_json}}

Your task:
- Suggest relevant interview questions or skill assessments tailored to the job role and candidate's background.
- Output a JSON object with fields: 'interview_questions' and 'skill_assessments'.
- Each entry in the interview_questions array should be an object containing the subfields category and question.
- Similarly, each entry in the skill_assessments array should be an object containing the subfields assessment_type, description, and rationale.
""",
    generate_content_config=types.GenerateContentConfig(temperature=0),
    output_key="interview_questions_json"
)
logger.info("Initialized interview_question_agent")

pipeline_agent = SequentialAgent(
    name="advanced_profile_jd_scoring_pipeline",
    description="Runs the full candidate-job matching, enrichment, compliance, recommendation, and dashboard pipeline.",
    sub_agents=[
        parallel_agent,                  # Resume & JD extraction
        match_agent,                     # Attribute scoring
        semantic_scoring_agent,          # Semantic scoring
        final_ranking_agent,             # Final ranking
        external_hr_enrichment_agent,    # Enrich profile from HR systems
        gap_flagging_agent,              # Flag gaps/mismatches
        interview_question_agent,        # Suggest interview questions
        merge_context_agent,             # Merge all context variables into a single JSON object
        save_context_agent,              # Save the final merged context JSON
    ],
)
logger.info("Initialized pipeline_agent")

root_agent = Agent(
    name="root_agent",
    model=model_name,
    description=(
        "Coordinates the end-to-end candidate-job matching workflow: extracts and structures resume and job description, computes match scores, aggregates results, enriches candidate data, flags profile gaps, and displays all intermediate and final results."
    ),
    global_instruction=(
        "You are a candidate-job matching assistant. Accept a resume file path and job description, extract and structure both, compute and aggregate match scores, enrich the profile using external HR systems, flag gaps, and display all intermediate and final results."
    ),
    instruction="""
    1. Accept a resume file path and job description from the user.
    2. Store them as 'profile_path' and 'job_description'.
    3. Run the pipeline_agent to:
        a. Extract and structure resume and job description.
        a1. Display the extracted resume text and job description.
        b. Compute and display attribute and semantic match scores.
        c. Aggregate results for a final ranking.
        d. Enrich the profile using external HR systems.
        e. Flag and display profile gaps.
        f. Merge all context variables into a single JSON object.
        g. Save the final merged context JSON to a file named based on the profile_path.
    4. Return all intermediate and final results in JSON format.
    5. Display an error message if any step fails.
    6. Save the final merged context JSON to a file and Profile_path base  name as the filename.
    7. The final output will be a JSON object containing all the merged context variables, including:
       - Profile data
       - Attribute scores
       - Semantic match
       - Final ranking
       - Enriched profile data
       - Flagged gaps
       - Interview questions
    """,
    sub_agents=[pipeline_agent],
    output_key="merged_context_json",
)
logger.info("Initialized root_agent")

logger.info("All agents initialized and pipeline constructed.")