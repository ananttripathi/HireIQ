from langgraph.graph import StateGraph, END
from graph.state import GraphState
from agents.search_screen_agent import extract_resume, score_jobs
from agents.cover_letter_agent import generate_cover_letter
from agents.ats_agent import run_ats_analysis
from tools.tavily_tool import fetch_tavily_jobs
from tools.adzuna_tool import fetch_adzuna_jobs
from tools.pre_filter import pre_filter_jobs
from tools.report_generator import generate_report
from tools.tracker import log_application


def resume_extractor_node(state: GraphState) -> GraphState:
    profile = extract_resume(state["resume_text"])
    return {**state, "resume_profile": profile}


def job_fetcher_node(state: GraphState) -> GraphState:
    tavily_jobs = fetch_tavily_jobs(state["search_query"])
    adzuna_jobs = fetch_adzuna_jobs(state["search_query"])
    return {**state, "raw_jobs": tavily_jobs + adzuna_jobs}


def pre_filter_node(state: GraphState) -> GraphState:
    filtered = pre_filter_jobs(state["raw_jobs"], state["resume_profile"])
    return {**state, "filtered_jobs": filtered}


def score_jobs_node(state: GraphState) -> GraphState:
    scored = score_jobs(state["filtered_jobs"], state["resume_profile"])
    return {**state, "scored_jobs": scored}


def cover_letter_node(state: GraphState) -> GraphState:
    letter = generate_cover_letter(state["selected_job"], state["resume_profile"])
    return {**state, "cover_letter": letter}


def ats_node(state: GraphState) -> GraphState:
    analysis = run_ats_analysis(state["selected_job"], state["resume_profile"])
    return {**state, "ats_analysis": analysis}


def report_node(state: GraphState) -> GraphState:
    path = generate_report(state)
    return {**state, "report_path": path}


def tracker_node(state: GraphState) -> GraphState:
    if state.get("selected_job"):
        log_application(state["selected_job"])
    return state


def build_pipeline() -> StateGraph:
    workflow = StateGraph(GraphState)

    workflow.add_node("resume_extractor", resume_extractor_node)
    workflow.add_node("job_fetcher", job_fetcher_node)
    workflow.add_node("pre_filter", pre_filter_node)
    workflow.add_node("score_jobs", score_jobs_node)
    workflow.add_node("cover_letter", cover_letter_node)
    workflow.add_node("ats", ats_node)
    workflow.add_node("report", report_node)
    workflow.add_node("tracker", tracker_node)

    # Fan-out: resume extraction and job fetching run in parallel
    workflow.set_entry_point("resume_extractor")
    workflow.add_edge("resume_extractor", "pre_filter")
    workflow.add_edge("job_fetcher", "pre_filter")
    workflow.add_edge("pre_filter", "score_jobs")
    workflow.add_edge("score_jobs", END)

    # Second phase: user selects a job, then cover letter + ATS run
    workflow.add_edge("cover_letter", "ats")
    workflow.add_edge("ats", "report")
    workflow.add_edge("report", "tracker")
    workflow.add_edge("tracker", END)

    return workflow.compile()


search_graph = build_pipeline()
