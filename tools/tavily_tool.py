import os
import requests
from graph.state import JobListing

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")
TAVILY_URL = "https://api.tavily.com/search"


def fetch_tavily_jobs(query: str, max_results: int = 20) -> list[JobListing]:
    if not TAVILY_API_KEY:
        return []

    payload = {
        "api_key": TAVILY_API_KEY,
        "query": f"job listing {query}",
        "search_depth": "advanced",
        "max_results": max_results,
        "include_answer": False,
    }

    try:
        resp = requests.post(TAVILY_URL, json=payload, timeout=15)
        resp.raise_for_status()
        results = resp.json().get("results", [])
    except Exception:
        return []

    jobs = []
    for r in results:
        jobs.append(JobListing(
            title=r.get("title", "Unknown Role"),
            company=r.get("domain", "Unknown Company"),
            location="Not specified",
            description=r.get("content", ""),
            url=r.get("url", ""),
            source="tavily",
        ))
    return jobs
