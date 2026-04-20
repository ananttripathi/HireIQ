import json
import os
from datetime import datetime
from graph.state import ScoredJob

TRACKER_PATH = "outputs/applications.json"


def log_application(job: ScoredJob) -> None:
    os.makedirs("outputs", exist_ok=True)

    try:
        with open(TRACKER_PATH) as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "fit_score": job.fit_score,
        "url": job.url,
    }
    data.append(entry)

    with open(TRACKER_PATH, "w") as f:
        json.dump(data, f, indent=2)


def load_applications() -> list[dict]:
    try:
        with open(TRACKER_PATH) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
