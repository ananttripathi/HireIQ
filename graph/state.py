from typing import TypedDict, Optional
from pydantic import BaseModel, Field


class JobListing(BaseModel):
    title: str
    company: str
    location: str
    description: str
    url: str
    source: str = "unknown"
    salary: Optional[str] = None


class ScoredJob(BaseModel):
    title: str
    company: str
    location: str
    url: str
    fit_score: int = Field(ge=1, le=10)
    reasoning: str
    salary: Optional[str] = None


class ResumeProfile(BaseModel):
    skills: list[str]
    experience_years: int
    seniority: str
    roles: list[str]
    industries: list[str]
    raw_text: str


class CoverLetter(BaseModel):
    content: str
    word_count: int


class ATSAnalysis(BaseModel):
    missing_keywords: list[str]
    present_keywords: list[str]
    suggestions: list[str]


class ScoredJobList(BaseModel):
    jobs: list[ScoredJob]


class GraphState(TypedDict):
    resume_text: str
    search_query: str
    resume_profile: Optional[ResumeProfile]
    raw_jobs: Optional[list[JobListing]]
    filtered_jobs: Optional[list[JobListing]]
    scored_jobs: Optional[list[ScoredJob]]
    selected_job: Optional[ScoredJob]
    cover_letter: Optional[CoverLetter]
    ats_analysis: Optional[ATSAnalysis]
    report_path: Optional[str]
    error: Optional[str]
