import os
import requests
from graph.state import JobListing

ADZUNA_APP_ID = os.environ.get("ADZUNA_APP_ID", "")
ADZUNA_APP_KEY = os.environ.get("ADZUNA_APP_KEY", "")
ADZUNA_URL = "https://api.adzuna.com/v1/api/jobs/us/search/1"


def fetch_adzuna_jobs(query: str, max_results: int = 20) -> list[JobListing]:
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        return []

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "what": query,
        "results_per_page": max_results,
        "content-type": "application/json",
    }

    try:
        resp = requests.get(ADZUNA_URL, params=params, timeout=15)
        resp.raise_for_status()
        results = resp.json().get("results", [])
    except Exception:
        return []

    jobs = []
    for r in results:
        salary = None
        if r.get("salary_min") and r.get("salary_max"):
            salary = f"${int(r['salary_min']):,} - ${int(r['salary_max']):,}"

        jobs.append(JobListing(
            title=r.get("title", "Unknown Role"),
            company=r.get("company", {}).get("display_name", "Unknown Company"),
            location=r.get("location", {}).get("display_name", "Not specified"),
            description=r.get("description", ""),
            url=r.get("redirect_url", ""),
            source="adzuna",
            salary=salary,
        ))
    return jobs
