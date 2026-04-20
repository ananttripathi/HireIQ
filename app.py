import gradio as gr
from graph.pipeline import search_graph
from graph.state import GraphState

DESCRIPTION = """
Paste your resume, enter a job search query, and let HireIQ do the work.

**What happens:**
1. Your resume is parsed in parallel with live job fetching (Tavily + Adzuna)
2. Irrelevant roles are filtered by keyword heuristics — no wasted LLM calls
3. Remaining roles are scored 1-10 against your profile with reasoning
4. Select a role to generate a cover letter and ATS keyword gap analysis

**Free, no credit card:** Groq (LLaMA 3.3 70B) · DuckDuckGo Search · Adzuna
"""


def run_search(resume_text: str, search_query: str):
    if not resume_text.strip():
        return "Please paste your resume.", "", ""
    if not search_query.strip():
        return "Please enter a search query (e.g. 'Senior Python Engineer remote').", "", ""

    state: GraphState = {
        "resume_text": resume_text,
        "search_query": search_query,
        "resume_profile": None,
        "raw_jobs": None,
        "filtered_jobs": None,
        "scored_jobs": None,
        "selected_job": None,
        "cover_letter": None,
        "ats_analysis": None,
        "report_path": None,
        "error": None,
    }

    try:
        result = search_graph.invoke(state)
    except Exception as e:
        return f"Pipeline error: {e}", "", ""

    scored_jobs = result.get("scored_jobs") or []
    if not scored_jobs:
        return "No matching jobs found. Try a broader search query.", "", ""

    lines = [f"## Top {min(len(scored_jobs), 10)} Roles\n"]
    for i, job in enumerate(scored_jobs[:10], 1):
        salary = f" | {job.salary}" if job.salary else ""
        lines.append(
            f"**{i}. {job.title}** @ {job.company} ({job.location}){salary}\n"
            f"Fit Score: **{job.fit_score}/10** — {job.reasoning}\n"
            f"[Apply]({job.url})\n"
        )

    profile = result.get("resume_profile")
    profile_summary = ""
    if profile:
        profile_summary = (
            f"**Detected Profile:** {profile.seniority.title()} | "
            f"{profile.experience_years} years | "
            f"Skills: {', '.join(profile.skills[:8])}"
        )

    stats = (
        f"Fetched {len(result.get('raw_jobs') or [])} jobs | "
        f"After pre-filter: {len(result.get('filtered_jobs') or [])} | "
        f"Scored: {len(scored_jobs)}"
    )

    return "\n".join(lines), profile_summary, stats


def run_cover_letter_and_ats(resume_text: str, job_title: str, company: str, reasoning: str, url: str):
    from graph.state import ScoredJob, ResumeProfile
    from agents.search_screen_agent import extract_resume
    from agents.cover_letter_agent import generate_cover_letter
    from agents.ats_agent import run_ats_analysis

    if not resume_text.strip() or not job_title.strip():
        return "Missing resume or job title.", ""

    try:
        profile = extract_resume(resume_text)
        job = ScoredJob(
            title=job_title, company=company, location="", url=url,
            fit_score=8, reasoning=reasoning
        )
        letter = generate_cover_letter(job, profile)
        ats = run_ats_analysis(job, profile)
    except Exception as e:
        return f"Error: {e}", ""

    cover_text = letter.content
    ats_text = (
        f"**Missing keywords:** {', '.join(ats.missing_keywords)}\n\n"
        f"**Already present:** {', '.join(ats.present_keywords)}\n\n"
        "**Where to add them:**\n" + "\n".join(f"- {s}" for s in ats.suggestions)
    )
    return cover_text, ats_text


with gr.Blocks(title="HireIQ") as demo:
    gr.Markdown("# HireIQ — Agentic Job Hunting Assistant")
    gr.Markdown(DESCRIPTION)

    with gr.Tab("Search & Score"):
        with gr.Row():
            resume_input = gr.Textbox(label="Your Resume", lines=15, placeholder="Paste your full resume here...")
            search_input = gr.Textbox(label="Search Query", lines=2, placeholder="e.g. Senior Python Engineer remote")

        search_btn = gr.Button("Find & Score Jobs", variant="primary")
        profile_out = gr.Markdown(label="Detected Profile")
        stats_out = gr.Markdown(label="Pipeline Stats")
        results_out = gr.Markdown(label="Scored Jobs")

        search_btn.click(
            fn=run_search,
            inputs=[resume_input, search_input],
            outputs=[results_out, profile_out, stats_out],
        )

    with gr.Tab("Cover Letter & ATS"):
        gr.Markdown("Fill in the role details from a job you want to apply to.")
        with gr.Row():
            cl_resume = gr.Textbox(label="Your Resume", lines=12, placeholder="Paste resume...")
            with gr.Column():
                cl_title = gr.Textbox(label="Job Title")
                cl_company = gr.Textbox(label="Company")
                cl_reasoning = gr.Textbox(label="Why this role interests you (optional)")
                cl_url = gr.Textbox(label="Job URL (optional)")

        cl_btn = gr.Button("Generate Cover Letter + ATS Analysis", variant="primary")
        cover_out = gr.Textbox(label="Cover Letter", lines=15)
        ats_out = gr.Markdown(label="ATS Keyword Gap")

        cl_btn.click(
            fn=run_cover_letter_and_ats,
            inputs=[cl_resume, cl_title, cl_company, cl_reasoning, cl_url],
            outputs=[cover_out, ats_out],
        )

if __name__ == "__main__":
    demo.launch()
