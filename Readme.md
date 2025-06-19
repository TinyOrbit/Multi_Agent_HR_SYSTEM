# HR Resume Multi-Agent API

A robust, container-ready FastAPI application for extracting, processing, and analyzing resumes using a multi-agent system powered by Google ADK and Gemini models. This project automates resume parsing, job description matching, candidate ranking, enrichment (e.g., LinkedIn), gap flagging, and interview question generation.

---

## Features

- **Multi-Agent Orchestration:** Modular pipeline using Google ADK agents (sequential, parallel, and LLM agents).
- **Resume Extraction:** Extracts text from PDF resumes.
- **Resume Structuring:** Converts unstructured text into structured JSON using a Pydantic schema.
- **Job Description Parsing:** Extracts requirements and skills from job descriptions.
- **Profile & JD Matching:** Attribute and semantic scoring between candidate and job.
- **External Enrichment:** Fetches additional candidate info (e.g., LinkedIn).
- **Gap Analysis:** Flags missing or mismatched skills/certifications.
- **Interview Question Generation:** Suggests tailored interview questions.
- **Session Management:** Persistent session IDs for continuity across container restarts.
- **Cloud Logging:** Integrated with Google Cloud Logging for observability.
- **Container-Ready:** Includes Dockerfile for easy deployment.

---

## Project Structure

```
modular_code/
│
├── app.py                # FastAPI app entrypoint
├── requirements.txt      # Python dependencies
├── dockerfile            # Container build instructions
│
└── src/
    ├── agents.py         # All agent and pipeline definitions
    ├── tools.py          # Tool functions (file extraction, enrichment, etc.)
    └── schema.py         # Pydantic schemas for input/output
```

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/TinyOrbit/Multi_Agent_HR_SYSTEM.git
cd modular_code
```

### 2. Set Up Environment

- Create a `.env` file with required environment variables (e.g., `MODEL`, Google credentials, etc.).
- Example:
  ```
        GOOGLE_GENAI_USE_VERTEXAI=TRUE
        GOOGLE_CLOUD_PROJECT=<PROJECT>
        GOOGLE_CLOUD_LOCATION=<LOCATION>
        MODEL=gemini-2.0-flash-001
  ```

### 3. Build and Run with Docker

```bash
docker build -t hr-multiagent-api .
docker run -p 8000:8000 --env-file .env -v $(pwd):/app hr-multiagent-api
```

### 4. API Usage

- The main endpoint is:
  ```
  POST /multi_agent_call
  ```
  **Request Body Example:**
  ```json
  {
    "profile_path": "path/to/resume.pdf",
    "job_description": {
      "title": "Welder",
      "skills": ["Welding", "Blueprint Reading"],
      "experience": "2+ years"
    }
  }
  ```

- **Response:**  
  Returns structured candidate-job matching results, including all intermediate and final outputs.

- **Interactive Docs:**  
  Visit [http://localhost:8000/docs](http://localhost:8000/docs) after running the container.

---

## Development

- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- Run locally:
  ```bash
  uvicorn app:app --reload
  ```

---

## Configuration & Customization

- **Agents:**  
  Modify or extend agents in `src/agents.py` for custom workflows.
- **Tools:**  
  Add new tools or update existing ones in `src/tools.py`.
- **Schemas:**  
  Update `src/schema.py` to change input/output formats.

---

## Session Management

- Session IDs are persisted in `session_ids.json` for continuity across container restarts.
- For multi-container deployments, consider using a shared session store (e.g., Redis, Cloud SQL).

---

## Logging

- Integrated with Google Cloud Logging.
- All major events and errors are logged for observability.

---

## Testing

- Run tests with:
  ```bash
  pytest
  ```

---

## Deployment

- Ready for deployment on any container platform (Docker, Kubernetes, Cloud Run, etc.).
- For Azure or GCP deployment, follow best practices for secrets and persistent storage.

---

## License

MIT License

---

## Acknowledgements

- [Google ADK](https://ai.google.dev/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Gemini Models](https://ai.google.dev/gemini)