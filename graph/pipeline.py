from concurrent.futures import ThreadPoolExecutor
from langgraph.graph import StateGraph, END
from graph.state import GraphState
from agents.search_screen_agent import extract_resume, score_jobs
from tools.tavily_tool import fetch_tavily_jobs
from tools.adzuna_tool import fetch_adzuna_jobs
from tools.pre_filter import pre_filter_jobs


def _fetch_jobs(query: str):
    with ThreadPoolExecutor(max_workers=2) as ex:
        f1 = ex.submit(fetch_tavily_jobs, query)
        f2 = ex.submit(fetch_adzuna_jobs, query)
        return f1.result() + f2.result()


def fetch_all_node(state: GraphState) -> GraphState:
    """Resume extraction and job fetching run in parallel."""
    with ThreadPoolExecutor(max_workers=2) as ex:
        f_profile = ex.submit(extract_resume, state["resume_text"])
        f_jobs    = ex.submit(_fetch_jobs, state["search_query"])
        profile   = f_profile.result()
        raw_jobs  = f_jobs.result()
    return {**state, "resume_profile": profile, "raw_jobs": raw_jobs}


def pre_filter_node(state: GraphState) -> GraphState:
    filtered = pre_filter_jobs(state["raw_jobs"], state["resume_profile"])
    return {**state, "filtered_jobs": filtered}


def score_jobs_node(state: GraphState) -> GraphState:
    scored = score_jobs(state["filtered_jobs"], state["resume_profile"])
    return {**state, "scored_jobs": scored}


def build_search_pipeline():
    workflow = StateGraph(GraphState)
    workflow.add_node("fetch_all",   fetch_all_node)
    workflow.add_node("pre_filter",  pre_filter_node)
    workflow.add_node("score_jobs",  score_jobs_node)

    workflow.set_entry_point("fetch_all")
    workflow.add_edge("fetch_all",  "pre_filter")
    workflow.add_edge("pre_filter", "score_jobs")
    workflow.add_edge("score_jobs", END)
    return workflow.compile()


search_graph = build_search_pipeline()
