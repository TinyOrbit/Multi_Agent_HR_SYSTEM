import os
import io
import json
import datetime
import logging

from dotenv import load_dotenv
import google.cloud.logging
from google.cloud import storage
from google.cloud import bigquery
from PyPDF2 import PdfReader

# --- Logging Setup ---
cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()
logger = logging.getLogger(__name__)

# --- Environment Setup ---
load_dotenv()
model_name = os.getenv("MODEL")
logger.info(f"Loaded model: {model_name}")




# --- BigQuery Insertion ---
def json_to_bigquery(json_file):
    try:
        client = bigquery.Client()
        dataset_id = 'candidate_cv'
        table_id = 'welder_profile_v1'
        table_ref = client.dataset(dataset_id).table(table_id)

        # Accept both dict and str input
        if isinstance(json_file, str):
            import json
            try:
                data = json.loads(json_file)
            except Exception as e:
                logger.error(f"Failed to parse JSON string: {e}")
                return {"error": f"Invalid JSON string: {e}"}
        elif isinstance(json_file, dict):
            data = json_file
        else:
            logger.error("Input must be a JSON string or dictionary.")
            return {"error": "Input must be a JSON string or dictionary."}

        # Ensure data is a list of dictionaries
        if isinstance(data, dict):
            data = [data]
        elif not isinstance(data, list):
            logger.error("Parsed data is not a list or dict.")
            return {"error": "Parsed data is not a list or dict."}

        errors = client.insert_rows_json(table_ref, data)
        if errors:
            logger.error(f"BigQuery insertion errors: {errors}")
            return {"error": f"BigQuery insertion errors: {errors}"}
        else:
            logger.info("Data inserted successfully into BigQuery.")
            return {"success": True}
    except Exception as e:
        logger.exception(f"Exception during BigQuery insertion: {e}")
        return {"error": f"Exception during BigQuery insertion: {e}"}

def fetch_linkedin_profile(linkedin_url: str):
    """
    Fetch candidate info from LinkedIn using ProxyCurl API.
    """
    if not isinstance(linkedin_url, str) or not linkedin_url:
        logger.error("Invalid LinkedIn URL provided.")
        return {"error": "Invalid LinkedIn URL."}
    # Uncomment and configure for real API usage
    # try:
    #     LINKEDIN_API_KEY = os.getenv("PROXYCURL_API_KEY")
    #     if not LINKEDIN_API_KEY:
    #         logger.error("LinkedIn API KEY not found.")
    #         return {"error": "LinkedIn API KEY not found."}
    #     endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    #     headers = {'Authorization': f'Bearer {LINKEDIN_API_KEY}'}
    #     params = {'linkedin_profile_url': linkedin_url}
    #     response = requests.get(endpoint, headers=headers, params=params)
    #     if response.status_code == 200:
    #         return response.json()
    #     else:
    #         logger.error(f"LinkedIn API error: {response.status_code} {response.text}")
    #         return {"error": f"LinkedIn API error: {response.status_code} {response.text}"}
    # except Exception as e:
    #     logger.exception(f"Exception during LinkedIn fetch: {e}")
    #     return {"error": f"Exception during LinkedIn fetch: {e}"}
    return {"info": "LinkedIn fetch simulated. API call not implemented."}




# --- JSON Conversion for GH ---
def convert_gh_to_modified_json(input_json):
    if not isinstance(input_json, dict):
        raise ValueError("Input to convert_gh_to_modified_json must be a dict.")
    modified_json = {}
    profile = input_json.get("int_profile_data_json", {})
    if "skills" in profile and isinstance(profile["skills"], list):
        profile["skills"] = ", ".join([str(skill) for skill in profile["skills"]])
    modified_json.update(profile)
    attribute_scores = input_json.get("attribute_scores", {})
    modified_json.update(attribute_scores)
    semantic_match = input_json.get("semantic_match", {})
    modified_json.update(semantic_match)
    interview_data = input_json.get("interview_questions_json", {})
    if isinstance(interview_data, dict) and "interview_questions" in interview_data:
        questions = interview_data.get("interview_questions", [])
        for q in questions:
            if isinstance(q, dict):
                q.pop("rationale", None)
    modified_json.update(interview_data)
    final_ranking = input_json.get("final_ranking", {})
    for key, value in final_ranking.items():
        if key not in modified_json:
            modified_json[key] = value
        elif key == "ranking" and "ranking_summary" not in modified_json:
            modified_json["ranking_summary"] = final_ranking.get("summary", "")
    enriched_profile = input_json.get("enriched_profile_json", {})
    if "linkedin_profile" in enriched_profile:
        modified_json["linkedin_profile"] = enriched_profile["linkedin_profile"]
    flagged_gaps = input_json.get("flagged_gaps_json", {})
    flagged_issues = flagged_gaps.get("flagged_issues", [])
    if flagged_issues:
        modified_json["flagged_issue"] = ",".join([issue.get("issue", "") for issue in flagged_issues])
        modified_json["flagged_issue_description"] = ",".join([issue.get("description", "") for issue in flagged_issues])
        modified_json["flagged_issue_severity"] = ",".join([issue.get("severity", "") for issue in flagged_issues])
        modified_json["flagged_issue_resolution"] = ",".join([issue.get("resolution", "") for issue in flagged_issues])
    return modified_json



# --- Save Context to JSON and BigQuery ---
def save_context_to_json(context_data: dict, output_key: str):
    """
    Save context data to BigQuery only.
    """
    try:
        if not isinstance(context_data, dict):
            logger.error("Context data must be a dictionary.")
            return {"error": "Context data must be a dictionary."}
        
        result = json_to_bigquery(context_data)
        logger.info("Context saved to BigQuery.")
        return result
    except Exception as e:
        logger.exception(f"Error saving context to BigQuery: {e}")
        return {"error": f"Error saving context to BigQuery: {e}"}

# --- Extract Text from Local File ---
def extract_text_from_file(file_path: str):
    try:
        if not isinstance(file_path, str) or not file_path:
            logger.error("Invalid file path provided.")
            return {"error": "Invalid file path."}
        if file_path.lower().endswith(".pdf"):
            try:
                reader = PdfReader(file_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                logger.info(f"Extracted text from PDF: {file_path}")
                return text
            except Exception as e:
                logger.exception(f"Error reading PDF file: {e}")
                return {"error": f"Error reading PDF file: {e}"}
        else:
            logger.error("Unsupported file type.")
            return {"error": "Unsupported file type. Only PDF supported in this example."}
    except Exception as e:
        logger.exception(f"Exception during file extraction: {e}")
        return {"error": f"Exception during file extraction: {e}"}

# --- Extract Texts from GCS Bucket ---
def extract_texts_from_gcs(bucket_name, prefix, service_account_json, archive_prefix="archive_cv/"):
    try:
        client = storage.Client.from_service_account_json(service_account_json)
        bucket = client.get_bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)
        texts = {}
        for blob in blobs:
            try:
                content = blob.download_as_text()
                texts[blob.name] = content
                logger.info(f"Extracted text from GCS blob: {blob.name}")
            except Exception as e:
                logger.error(f"Error downloading blob {blob.name}: {e}")
                texts[blob.name] = f"Error: {e}"
        return texts
    except Exception as e:
        logger.exception(f"Exception during GCS extraction: {e}")
        return {"error": f"Exception during GCS extraction: {e}"}