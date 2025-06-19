# Process to Run the Code.


### To test locally:

```python
python -m venv venv
```
```python
source venv\bin\activate  
```
OR 
```
.\.venv\Scripts\activate
```

```python
pip install -r requirements.txt
```

```python
uvicorn app:app --reload
```


```
use <endpoints>.com/multi_agent_call  
```
OR

```
visit <endpoints>.com/docs choose --> multi_agent_call
```
PASTE THE INPUT IN FOLLOWING FORMAT:

### INPUT

```json
{
  "profile_path": "../data/cv_electricians_resume_lisa_ray_Master_Electrician 1.docx",
  "job_description": {
    "job_title": "Electrician",
    "job_summary": "Responsible for installing, maintaining, and repairing electrical control, wiring, and lighting systems. Ensures that electrical installations and systems work efficiently and safely.",
    "duties_and_responsibilities": [
      "Install, maintain, and repair electrical control, wiring, and lighting systems.",
      "Read blueprints and technical diagrams.",
      "Inspect electrical components, such as transformers and circuit breakers.",
      "Identify electrical problems with a variety of testing devices.",
      "Follow state and local building regulations based on the National Electric Code.",
      "Direct and train workers to install, maintain, or repair electrical wiring or equipment.",
      "Ensure compliance with codes for safety and efficiency.",
      "Test electrical systems and continuity of circuits in electrical wiring, equipment, and fixtures using testing devices to ensure compatibility and safety.",
      "Diagnose malfunctioning systems and components, using test equipment, to locate the cause of a breakdown and correct the problem.",
      "Connect wires to circuit breakers, transformers, or other components.",
      "Advise management on whether continued operation of equipment could be hazardous.",
      "Perform business management duties such as maintaining records and files, preparing reports, and ordering supplies and equipment."
    ],
    "skills_and_qualifications": [
      "Proven experience as an electrician.",
      "Experience in industrial and/or commercial electrical systems.",
      "Demonstrable ability to use electrical and hand tools (e.g. wire strippers, voltmeter, etc.) and electrical drawings and blueprints.",
      "Thorough knowledge of safety procedures and legal regulations and guidelines.",
      "Excellent critical thinking and problem-solving ability.",
      "Good physical condition and flexibility to work long shifts and overnight."
    ],
    "education_and_experience": [
      "High school diploma or equivalent.",
      "Completion of an electrician apprenticeship program.",
      "Valid electrician license."
    ],
    "work_environment": "Work in residential, commercial, and industrial settings. May involve working in confined spaces, at heights, and in various weather conditions.",
    "salary_range": "Based on experience and qualifications.",
    "benefits": [
      "Health insurance",
      "Paid time off",
      "Retirement plan",
      "Professional development assistance"
    ]
  }
}

```

### OUTPUT:

```json
{
  "response": {
    "certification_match": 0,
    "certifications": [
      {
        "certificate_url": "https://www.indeed.com/career-advice/resume-samples/manufacturing-and-maintenance-resumes 1/2Skills",
        "name": "Project Management Professional",
        "provider": "Project Management Institute - 20206/12/25"
      }
    ],
    "education": [
      {
        "degree": "Associate of Applied Science in industrial maintenance",
        "institution": "Northern Sandhills Community College"
      }
    ],
    "education_match": 0,
    "email": "ismith@email.com",
    "experience": [
      {
        "company": "AME Industries, Omaha, NE",
        "description": "Identify and troubleshoot equipment malfunctions quickly to minimize downtime, contributing to\\nthe team\\'s 98% ef ficiency record\\nMaintain detailed records when inspecting and repairing equipment to prepare maintenance\\nreports\\nPurchase parts and supplies using a $10K maintenance budget to ensure fiscal responsibility\\nSupervise a team of five mechanics, communicating ef fectively to explain assignments and\\nexpectations",
        "job_title": "Maintenance Mechanic Supervisor",
        "start_year": "November 2017"
      },
      {
        "company": "Building W orks Manufacturing, Omaha, NE",
        "description": "Inspected and repaired mechanical equipment in a timely manner to keep it operating correctly\\nTrained six new maintenance employees on company policies to help them acquire skills\\nCompleted work orders and equipment logs in a computerized system to maintain records",
        "job_title": "Maintenance\\nMechanic",
        "start_year": "April 2014"
      },
      {
        "company": "Kornsky Manufacturing, Omaha, NE",
        "description": "Identified potential equipment malfunctions to fix problems proactively , saving an estimated $8K in\\ncomplex repairs\\nInstalled, fabricated and maintained equipment by reading instruction manuals and blueprints\\nMaintained comprehensive knowledge of safety regulations to ensure compliance",
        "job_title": "Maintenance Mechanic",
        "start_year": "February 201 1"
      }
    ],
    "experience_match": 0.2,
    "explanation": "Ivy Smith\\'s background as a Maintenance Mechanic Supervisor and Project Management Professional doesn\\'t align well with the Electrician role. While she has experience with blueprints and safety regulations, the core electrical skills and licensing requirements are missing. The score reflects the limited overlap in skills and experience.",
    "final_score": 21.5,
    "flagged_issue": "Missing Electrician License,Lack of Electrician Apprenticeship,Insufficient Electrical Experience,Missing Core Electrical Skills,PMP Certification Irrelevant",
    "flagged_issue_description": "The job description requires a valid electrician license, which is not mentioned in the candidate\\'s resume. This is a mandatory requirement for the role.,The job description requires completion of an electrician apprenticeship program. The candidate\\'s resume indicates an Associate of Applied Science in industrial maintenance, but does not explicitly state completion of an electrician apprenticeship.,The candidate\\'s experience is primarily in maintenance mechanics, not specifically as an electrician. The job description requires proven experience as an electrician and experience in industrial and/or commercial electrical systems.,The resume does not explicitly list skills related to electrical systems, such as wiring, transformer maintenance, circuit breaker inspection, or knowledge of the National Electric Code (NEC).,The candidate highlights their Project Management Professional (PMP) certification, which is not directly relevant to the core duties of an electrician.",
    "flagged_issue_resolution": "Verify if the candidate possesses a valid electrician license not explicitly stated in the resume. If not, this is a critical disqualification.,Confirm with the candidate whether their industrial maintenance program included or was equivalent to a formal electrician apprenticeship. If not, further evaluation is needed to determine if their experience compensates for this requirement.,Assess the depth and breadth of the candidate\\'s electrical experience within their maintenance roles. Determine if their experience aligns with the \\'proven experience as an electrician\\' requirement. Request specific examples of electrical work performed.,Inquire about the candidate\\'s specific skills and experience related to electrical systems. Determine if they possess the necessary technical skills to perform the duties outlined in the job description.,While project management skills can be beneficial, prioritize the candidate\\'s electrical skills and experience. The PMP certification should not be a primary factor in the evaluation.",
    "flagged_issue_severity": "Critical,High,High,Medium,Low",
    "interview_questions": [
      {
        "category": "Technical Skills",
        "question": "This role requires a strong understanding of the National Electric Code (NEC). Can you describe your experience with NEC and how you ensure compliance in your work?"
      },
      {
        "category": "Technical Skills",
        "question": "The job involves diagnosing malfunctioning electrical systems. Can you walk me through your process for troubleshooting an electrical issue, from identification to resolution?"
      },
      {
        "category": "Experience",
        "question": "Your resume highlights experience as a Maintenance Mechanic. Can you provide specific examples of electrical work you\\'ve performed, detailing the types of systems you\\'ve worked on and the tools you\\'ve used?"
      },
      {
        "category": "Experience",
        "question": "The job description mentions working with transformers and circuit breakers. Can you describe your experience inspecting, maintaining, and repairing these components?"
      },
      {
        "category": "Safety",
        "question": "Safety is paramount in this role. Describe a time when you identified a potential electrical hazard and the steps you took to mitigate the risk."
      },
      {
        "category": "Apprenticeship",
        "question": "The job description requires completion of an electrician apprenticeship program. Can you elaborate on your training and experience in this area, and how it has prepared you for this role?"
      }
    ],
    "languages": [],
    "linkedin_profile": "not found",
    "location": "Omaha, NE",
    "name": "Ivy Smith",
    "overall_fit": 0.13,
    "phone": "402-555-0197",
    "projects": [],
    "ranking": "Low",
    "ranking_summary": "Ivy Smith\\'s background as a Maintenance Mechanic Supervisor and Project Management Professional doesn\\'t align well with the Electrician role. While she has experience with blueprints and safety regulations, the core electrical skills and licensing requirements are missing. The score reflects the limited overlap in skills and experience. The final score is 21.5, derived from a weighted average of attribute scores and semantic score.",
    "semantic_score": 30,
    "skill_assessments": [
      {
        "assessment_type": "Practical Assessment",
        "description": "Wire a simple circuit according to a provided schematic diagram.",
        "rationale": "Tests the candidate\\'s ability to read and interpret electrical schematics and demonstrate basic wiring skills."
      },
      {
        "assessment_type": "Knowledge Test",
        "description": "Administer a written test covering basic electrical theory, safety procedures, and NEC requirements.",
        "rationale": "Evaluates the candidate\\'s theoretical knowledge of electrical principles and safety regulations."
      },
      {
        "assessment_type": "Troubleshooting Simulation",
        "description": "Present the candidate with a simulated electrical fault and ask them to diagnose and propose a solution.",
        "rationale": "Assesses the candidate\\'s problem-solving skills and ability to apply their knowledge to real-world scenarios."
      }
    ],
    "skill_match": 0.33,
    "skills": "Machining, Hand and power tools, Fabrication technology, Budgeting, Project management, Safety regulations, Blueprints and schematics, Communication, Time management",
    "summary": "Highly skilled and hardworking Maintenance Mechanic with 10+ years of experience repairing\\nequipment to ensure seamless production processes. Adept at proactively performing maintenance\\nand conducting emergency repairs quickly to minimize downtime, resulting in 98% ef ficiency .\\nProject Management Professional (PMP) with experience supervising and leading teams to\\nachieve production goals."
  }
}
```



### OR with request module :

```python
import requests
import json

url = "<endpoint>.com/multi_agent_call"

payload = json.dumps({
  "profile_path": "../data/cv_electricians_resume_lisa_ray_Master_Electrician 1.docx",
  "job_description": {
    "job_title": "Electrician",
    "job_summary": "Responsible for installing, maintaining, and repairing electrical control, wiring, and lighting systems. Ensures that electrical installations and systems work efficiently and safely.",
    "duties_and_responsibilities": [
      "Install, maintain, and repair electrical control, wiring, and lighting systems.",
      "Read blueprints and technical diagrams.",
      "Inspect electrical components, such as transformers and circuit breakers.",
      "Identify electrical problems with a variety of testing devices.",
      "Follow state and local building regulations based on the National Electric Code.",
      "Direct and train workers to install, maintain, or repair electrical wiring or equipment.",
      "Ensure compliance with codes for safety and efficiency.",
      "Test electrical systems and continuity of circuits in electrical wiring, equipment, and fixtures using testing devices to ensure compatibility and safety.",
      "Diagnose malfunctioning systems and components, using test equipment, to locate the cause of a breakdown and correct the problem.",
      "Connect wires to circuit breakers, transformers, or other components.",
      "Advise management on whether continued operation of equipment could be hazardous.",
      "Perform business management duties such as maintaining records and files, preparing reports, and ordering supplies and equipment."
    ],
    "skills_and_qualifications": [
      "Proven experience as an electrician.",
      "Experience in industrial and/or commercial electrical systems.",
      "Demonstrable ability to use electrical and hand tools (e.g. wire strippers, voltmeter, etc.) and electrical drawings and blueprints.",
      "Thorough knowledge of safety procedures and legal regulations and guidelines.",
      "Excellent critical thinking and problem-solving ability.",
      "Good physical condition and flexibility to work long shifts and overnight."
    ],
    "education_and_experience": [
      "High school diploma or equivalent.",
      "Completion of an electrician apprenticeship program.",
      "Valid electrician license."
    ],
    "work_environment": "Work in residential, commercial, and industrial settings. May involve working in confined spaces, at heights, and in various weather conditions.",
    "salary_range": "Based on experience and qualifications.",
    "benefits": [
      "Health insurance",
      "Paid time off",
      "Retirement plan",
      "Professional development assistance"
    ]
  }
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

```


