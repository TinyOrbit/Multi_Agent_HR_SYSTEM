
from typing import List, Optional
from pydantic import BaseModel, Field

class EducationEntry(BaseModel):
    degree: str = Field(description="Degree or qualification obtained")
    institution: str = Field(description="Name of the educational institution")
    start_year: Optional[str] = Field(default=None, description="Year education started")
    end_year: Optional[str] = Field(default=None, description="Year education ended or expected to end")

class ExperienceEntry(BaseModel):
    job_title: str = Field(description="Job title or position held")
    company: str = Field(description="Name of the company or organization")
    start_year: Optional[str] = Field(default=None, description="Start date (YYYY-MM or similar)")
    start_year: Optional[str] = Field(default=None, description="End date or 'Present'")
    description: Optional[str] = Field(default=None, description="Brief description of responsibilities or achievements")

class CertificationEntry(BaseModel):
    name: str = Field(description="Name of the certification")
    provider: Optional[str] = Field(default=None, description="Name of the certification provider")
    certificate_url: Optional[str] = Field(default=None, description="URL to the certification")
    start_year: Optional[str] = Field(default=None, description="Start date of the certification (YYYY-MM or similar)")
    start_year: Optional[str] = Field(default=None, description="Expiration date of the certification (YYYY-MM or similar)")


class ResumeOutput(BaseModel):
    name: str = Field(description="Full name of the candidate")
    email: Optional[str] = Field(default=None, description="Email address")
    phone: Optional[str] = Field(default=None, description="Phone number")
    # address: Optional[str] = Field(default=None, description="Mailing address")
    location: Optional[str] = Field(default=None, description="Current location or city")
    summary: Optional[str] = Field(default=None, description="Professional summary or objective")
    skills: List[str] = Field(default_factory=list, description="List of skills")
    education: List[EducationEntry] = Field(default_factory=list, description="List of education entries")
    experience: List[ExperienceEntry] = Field(default_factory=list, description="List of work experience entries")
    certifications: List[CertificationEntry] = Field(default_factory=list, description="List of certifications")
    languages: List[str] = Field(default_factory=list, description="Languages spoken or known")
    projects: List[str] = Field(default_factory=list, description="Notable projects")
    linkedin: Optional[str] = Field(default=None, description="LinkedIn profile URL")
    github: Optional[str] = Field(default=None, description="GitHub profile URL")


class File_Inputs(BaseModel):
    profile_path: str = Field(description="Resume file path to extract text from.")
    job_description: dict = Field(description="Job description to match against the resume in json format.")
