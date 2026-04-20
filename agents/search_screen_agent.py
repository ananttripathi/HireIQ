import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import ResumeProfile, ScoredJob, JobListing, ScoredJobList

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

RESUME_EXTRACT_PROMPT = """You are a resume parser. Extract structured information from the resume below.
Return a JSON object with these exact keys:
- skills: list of technical skills (strings)
- experience_years: integer (total years of experience)
- seniority: one of "junior", "mid", "senior"
- roles: list of job titles the person has held
- industries: list of industries worked in
- raw_text: the full resume text unchanged

Resume:
{resume_text}"""

SCORE_PROMPT = """You are a hiring expert. Score this job listing against the candidate's profile.

Candidate Profile:
Skills: {skills}
Experience: {experience_years} years
Seniority: {seniority}
Past Roles: {roles}

Job Listing:
Title: {title}
Company: {company}
Location: {location}
Description: {description}

Return a JSON object with:
- fit_score: integer 1-10 (10 = perfect fit)
- reasoning: 1-2 sentence explanation"""


def extract_resume(resume_text: str) -> ResumeProfile:
    structured_llm = llm.with_structured_output(ResumeProfile)
    prompt = RESUME_EXTRACT_PROMPT.format(resume_text=resume_text)
    result = structured_llm.invoke([HumanMessage(content=prompt)])
    result.raw_text = resume_text
    return result


def score_jobs(jobs: list[JobListing], profile: ResumeProfile) -> list[ScoredJob]:
    if not jobs:
        return []

    structured_llm = llm.with_structured_output(ScoredJobList)

    job_entries = "\n\n".join(
        f"Job {i+1}:\nTitle: {j.title}\nCompany: {j.company}\nLocation: {j.location}\nDescription: {j.description[:800]}"
        for i, j in enumerate(jobs)
    )

    prompt = f"""You are a hiring expert. Score each job listing against this candidate profile.

Candidate:
Skills: {', '.join(profile.skills[:20])}
Experience: {profile.experience_years} years ({profile.seniority})
Past Roles: {', '.join(profile.roles[:5])}

Jobs to score:
{job_entries}

For each job return fit_score (1-10) and reasoning (1 sentence). Include title, company, location, url."""

    scored_list = structured_llm.invoke([HumanMessage(content=prompt)])
    scored = sorted(scored_list.jobs, key=lambda j: j.fit_score, reverse=True)

    for i, s in enumerate(scored):
        if i < len(jobs):
            s.url = jobs[i].url
            if jobs[i].salary:
                s.salary = jobs[i].salary

    return scored
