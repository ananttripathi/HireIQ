from graph.state import JobListing, ResumeProfile

JUNIOR_TERMS = {"junior", "entry level", "entry-level", "graduate", "intern", "internship", "jr."}
SENIOR_TERMS = {"senior", "sr.", "staff", "principal", "lead", "director", "head of", "vp", "manager"}


def _seniority_matches(title: str, seniority: str) -> bool:
    title_lower = title.lower()
    if seniority in ("junior", "mid"):
        return not any(term in title_lower for term in SENIOR_TERMS)
    if seniority == "senior":
        return not any(term in title_lower for term in JUNIOR_TERMS)
    return True


def pre_filter_jobs(jobs: list[JobListing], profile: ResumeProfile) -> list[JobListing]:
    if not jobs or not profile:
        return jobs or []

    seen_urls = set()
    filtered = []

    for job in jobs:
        if not job.description or len(job.description) < 50:
            continue

        if job.url in seen_urls:
            continue
        seen_urls.add(job.url)

        if not _seniority_matches(job.title, profile.seniority):
            continue

        filtered.append(job)

    return filtered[:30]
