import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from graph.state import ResumeExtract, ResumeProfile, ScoredJob, JobListing, SingleJobScore

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)


def extract_resume(resume_text: str) -> ResumeProfile:
    structured_llm = llm.with_structured_output(ResumeExtract)
    prompt = f"""Parse this resume and extract structured information.

Resume:
{resume_text}

Return:
- skills: list of technical skills (programming languages, frameworks, tools)
- experience_years: integer (total years of professional experience)
- seniority: exactly one of "junior", "mid", or "senior"
- roles: list of job titles held (e.g. "Software Engineer", "Data Scientist")
- industries: list of industries worked in"""

    extract = structured_llm.invoke([HumanMessage(content=prompt)])
    return ResumeProfile(**extract.model_dump(), raw_text=resume_text)


def _score_single(job: JobListing, profile: ResumeProfile) -> ScoredJob:
    structured_llm = llm.with_structured_output(SingleJobScore)
    prompt = f"""Score this job against the candidate profile. Be realistic and strict.

Candidate: {profile.seniority} · {profile.experience_years} years
Skills: {', '.join(profile.skills[:15])}
Past Roles: {', '.join(profile.roles[:5])}

Job: {job.title} at {job.company} ({job.location})
Description: {job.description[:700]}

Return fit_score (1–10, where 10 is a perfect match) and reasoning (one sentence, be specific)."""

    result = structured_llm.invoke([HumanMessage(content=prompt)])
    return ScoredJob(
        title=job.title,
        company=job.company,
        location=job.location,
        url=job.url,
        salary=job.salary,
        fit_score=result.fit_score,
        reasoning=result.reasoning,
    )


def score_jobs(jobs: list[JobListing], profile: ResumeProfile, max_jobs: int = 12) -> list[ScoredJob]:
    if not jobs:
        return []

    jobs = jobs[:max_jobs]
    scored = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(_score_single, job, profile): job for job in jobs}
        for future in as_completed(futures):
            try:
                scored.append(future.result(timeout=30))
            except Exception:
                pass

    return sorted(scored, key=lambda j: j.fit_score, reverse=True)
