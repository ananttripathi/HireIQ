---
title: HireIQ
emoji: 🎯
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 6.12.0
app_file: app.py
pinned: false
license: mit
---

# 🎯 HireIQ — Agentic Job Hunting Assistant

HireIQ is a multi-agent AI system that automates the most painful parts of job hunting. Paste your resume and a search query, and a crew of specialised agents finds relevant roles, scores them against your profile, writes a personalised cover letter, and tells you exactly which keywords to add to pass ATS filters.

## The Problem

Job hunting is exhausting and repetitive. Senior engineers spend hours:
- Searching across LinkedIn, Indeed, Wellfound, and company career pages separately
- Manually writing cover letters from scratch for each role
- Guessing whether their resume will pass ATS keyword filters
- Tracking applications with no structure across spreadsheets and browser tabs

## The Solution

3 focused AI agents that collaborate end-to-end:

```
User pastes resume + enters search query
        |
        v
Search + Screen Agent    Fetches jobs via JSearch + Adzuna APIs
                         Scores each role against your resume (1-10 fit score with reasoning)
        |
        v
User selects a role they want to apply for
        |
        v
Cover Letter Agent       Writes a personalised cover letter using your resume + the full JD
        |
        v
ATS Agent                Identifies missing keywords from the JD
                         Suggests exactly where to add them in your resume
                         (you decide what to change — no hallucinated edits)
        |
        v
Tracker                  Logs the role, fit score, and date to your application pipeline
```

## Why 3 Agents and Not 5

The original design had 5 agents including automated resume rewriting. That approach was dropped for two reasons:

1. Auto-rewriting resume bullets risks hallucinating experience you do not have — a recruiter will catch it
2. 5 sequential LLM calls on a free-tier API (Groq) is slow and hits rate limits fast on a public deployment

The 3-agent design does more with less: job discovery and scoring in a single pass, then cover letter and ATS analysis only for roles the user actually wants to pursue.

## Data Sources

| Source | API | Free Tier | What it provides |
|--------|-----|-----------|-----------------|
| JSearch (RapidAPI) | REST | 200 requests/day | Structured jobs from Indeed, LinkedIn, Glassdoor |
| Adzuna | REST | 200 calls/day | Full job descriptions, salary data |

No scraping. Both are legitimate APIs with structured data including full job descriptions — which is what the cover letter and ATS agents need to work well.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent orchestration | LangGraph |
| LLM | Groq (LLaMA 3.3 70B) — free |
| Job search | JSearch API + Adzuna API — free tier |
| Resume input | Plain text paste (no parsing bugs) |
| Persistence | JSON application tracker |
| UI | Gradio |
| Deployment | Hugging Face Spaces + GitHub Actions |

## Project Structure

```
HireIQ/
├── app.py                      # Gradio UI + LangGraph pipeline entry point
├── agents/
│   ├── search_screen_agent.py  # Fetches jobs from APIs, scores vs resume
│   ├── cover_letter_agent.py   # Generates personalised cover letter
│   └── ats_agent.py            # Keyword gap analysis vs resume
├── tools/
│   ├── jsearch_tool.py         # JSearch API wrapper
│   ├── adzuna_tool.py          # Adzuna API wrapper
│   └── tracker.py              # JSON application pipeline logger
├── outputs/                    # Generated cover letters + tracker JSON
├── requirements.txt
└── .github/
    └── workflows/
        └── deploy-hf.yml       # Auto-deploy to HF Spaces on push to main
```

## Setup

```bash
git clone https://github.com/ananttripathi/HireIQ.git
cd HireIQ
pip install -r requirements.txt
```

Set the following environment variables (or add as HF Space secrets):

```bash
GROQ_API_KEY=your_groq_api_key        # console.groq.com — free
JSEARCH_API_KEY=your_jsearch_key      # rapidapi.com/letscrape-6bfcf/api/jsearch — free tier
ADZUNA_APP_ID=your_adzuna_app_id      # developer.adzuna.com — free
ADZUNA_APP_KEY=your_adzuna_app_key
```

## Deploy to Hugging Face Spaces

1. Create a new Gradio Space at huggingface.co
2. Add the 4 API keys above as Space secrets under Settings
3. Add `HF_TOKEN` as a GitHub repo secret — CI/CD auto-deploys on every push to `main`

## License

[MIT](LICENSE)
