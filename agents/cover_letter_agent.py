from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import ScoredJob, ResumeProfile, CoverLetter

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.4)

SYSTEM_PROMPT = """You are an expert career coach writing cover letters. Write in first person, professional but warm tone.
- Keep it to 3-4 paragraphs, under 350 words
- Open with why this specific role excites the candidate
- Reference 2-3 concrete skills or experiences from the resume
- Close with a call to action
- Do NOT make up any experience or skills not in the resume"""


def generate_cover_letter(job: ScoredJob, profile: ResumeProfile) -> CoverLetter:
    prompt = f"""Write a cover letter for this application.

Role: {job.title} at {job.company} ({job.location})
Why this role: {job.reasoning}

Candidate background:
Skills: {', '.join(profile.skills[:15])}
Experience: {profile.experience_years} years
Past Roles: {', '.join(profile.roles[:5])}

Resume (for reference):
{profile.raw_text[:2000]}"""

    result = llm.invoke([SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=prompt)])
    content = result.content.strip()
    return CoverLetter(content=content, word_count=len(content.split()))
