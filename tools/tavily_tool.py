from graph.state import JobListing

try:
    from duckduckgo_search import DDGS
    _DDGS_AVAILABLE = True
except ImportError:
    _DDGS_AVAILABLE = False


def fetch_tavily_jobs(query: str, max_results: int = 20) -> list[JobListing]:
    if not _DDGS_AVAILABLE:
        return []

    search_query = f"{query} job opening site:linkedin.com OR site:indeed.com OR site:wellfound.com OR site:greenhouse.io"

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(search_query, max_results=max_results))
    except Exception:
        return []

    jobs = []
    for r in results:
        jobs.append(JobListing(
            title=r.get("title", "Unknown Role"),
            company=r.get("source", "Unknown Company"),
            location="Not specified",
            description=r.get("body", ""),
            url=r.get("href", ""),
            source="duckduckgo",
        ))
    return jobs
