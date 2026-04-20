from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import ScoredJob, ResumeProfile, ATSAnalysis

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

SYSTEM_PROMPT = """You are an ATS (Applicant Tracking System) expert.
Analyze the gap between a job description and a resume.
Return ONLY keywords and suggestions — never rewrite the resume bullets.
The candidate will decide what to write; you only tell them what is missing and where."""


def run_ats_analysis(job: ScoredJob, profile: ResumeProfile) -> ATSAnalysis:
    structured_llm = llm.with_structured_output(ATSAnalysis)

    prompt = f"""Analyze the ATS keyword gap for this application.

Job Title: {job.title} at {job.company}
Job Description / Reasoning: {job.reasoning}

Candidate Skills Already Present: {', '.join(profile.skills[:20])}

Resume Text (first 2000 chars):
{profile.raw_text[:2000]}

Return:
- missing_keywords: list of important keywords from JD not in resume (max 15)
- present_keywords: list of JD keywords already in resume (max 10)
- suggestions: list of specific advice on WHERE to add missing keywords (e.g. "Add 'Kubernetes' to your DevOps experience bullet in the XYZ role section")"""

    return structured_llm.invoke([SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=prompt)])
