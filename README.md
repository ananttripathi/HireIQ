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

3 focused AI agents orchestrated by LangGraph, running partially in parallel:

```
User pastes resume + enters search query
        |
        v
   [PARALLEL EXECUTION]
   /                    \
Resume Extractor      Job Fetcher
(Pydantic schema)     (Tavily + Adzuna APIs)
   \                    /
        Converge
        |
        v
Hybrid Pre-Filter         Fast keyword heuristics eliminate irrelevant roles
        |                 before any LLM calls (saves tokens + time)
        v
Search + Screen Agent     LLM scores remaining roles vs resume (1-10 + reasoning)
        |                 Structured output via Pydantic schema
        v
User selects a role
        |
        v
Cover Letter Agent        Personalised cover letter using resume + full JD
        |
        v
ATS Agent                 Keyword gap analysis — missing terms + where to add them
        |                 (user makes the final edits, no hallucinated rewrites)
        v
Report Generator          Markdown + PDF summary of results
        |
        v
Tracker                   Logs role, score, date to JSON application pipeline
```

## Architectural Decisions

### Why LangGraph over CrewAI
CrewAI relies on LangChain internals and its API has changed significantly across versions — the same instability that has affected the LangChain ecosystem broadly. LangGraph gives direct control over the state machine, supports parallel execution natively, and has a more stable API surface.

### Why Parallel Execution
Resume extraction and job fetching are completely independent. Running them in parallel via LangGraph fan-out/fan-in cuts the total pipeline time roughly in half before the LLM even starts scoring.

### Why Hybrid Pre-Filtering
Every LLM call costs time and tokens. A fast keyword check (seniority level, role type, location) eliminates clearly irrelevant listings before the scoring agent sees them. This pattern is used in production job search agents to handle rate limits on free-tier APIs.

### Why Pydantic Schemas for Every Agent Output
The most common failure mode in multi-agent systems is unpredictable LLM outputs breaking downstream agents. Every agent in HireIQ uses `.with_structured_output()` with a Pydantic model, so outputs are validated and typed before being passed to the next step.

### Why No Automated Resume Rewriting
Auto-rewriting resume bullets risks hallucinating experience the user does not have. Recruiters catch this. HireIQ does keyword gap analysis instead — it tells you what is missing and where to add it, but you decide what to write.

## Data Sources

| Source | API | Free Tier | What it provides |
|--------|-----|-----------|-----------------|
| Tavily | REST | 1,000 searches/month | Real-time job search across all major boards |
| Adzuna | REST | 200 calls/day | Full job descriptions with salary data |

Tavily is purpose-built for AI agents and returns clean, structured results optimised for LLM consumption — no HTML scraping, no rate-limit evasion, no ToS violations.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent orchestration | LangGraph |
| State management | GraphState TypedDict + Pydantic schemas |
| LLM | Groq (LLaMA 3.3 70B) — free |
| Structured output | `.with_structured_output()` on all agents |
| Job search | Tavily API + Adzuna API — free tier |
| Resume input | Plain text paste |
| Report output | Markdown + PDF (fpdf2) |
| Persistence | JSON application tracker |
| Observability | LangSmith (optional tracing) |
| UI | Gradio |
| Deployment | Hugging Face Spaces + GitHub Actions |

## Project Structure

```
HireIQ/
├── app.py                        # Gradio UI entry point
├── graph/
│   ├── state.py                  # GraphState TypedDict + all Pydantic output schemas
│   └── pipeline.py               # LangGraph workflow: nodes, edges, parallel fan-out
├── agents/
│   ├── search_screen_agent.py    # Scores jobs vs resume with structured output
│   ├── cover_letter_agent.py     # Generates personalised cover letter
│   └── ats_agent.py              # Keyword gap analysis vs resume
├── tools/
│   ├── tavily_tool.py            # Tavily API wrapper for job search
│   ├── adzuna_tool.py            # Adzuna API wrapper
│   ├── pre_filter.py             # Fast keyword heuristics before LLM scoring
│   ├── report_generator.py       # Markdown + PDF report output (fpdf2)
│   └── tracker.py                # JSON application pipeline logger
├── outputs/                      # Generated cover letters, reports, tracker JSON
├── requirements.txt
└── .github/
    └── workflows/
        └── deploy-hf.yml         # Auto-deploy to HF Spaces on push to main
```

## Setup

```bash
git clone https://github.com/ananttripathi/HireIQ.git
cd HireIQ
pip install -r requirements.txt
```

Set the following environment variables (or add as HF Space secrets):

```bash
GROQ_API_KEY=your_groq_api_key          # console.groq.com — free
TAVILY_API_KEY=your_tavily_api_key      # app.tavily.com — free 1000/month
ADZUNA_APP_ID=your_adzuna_app_id        # developer.adzuna.com — free
ADZUNA_APP_KEY=your_adzuna_app_key
LANGSMITH_API_KEY=your_langsmith_key    # optional — smith.langchain.com
```

## Deploy to Hugging Face Spaces

1. Create a new Gradio Space at huggingface.co
2. Add the API keys above as Space secrets under Settings
3. Add `HF_TOKEN` as a GitHub repo secret — CI/CD auto-deploys on every push to `main`

## Inspired By

Architecture patterns borrowed from:
- [sergio11/langgraph_jobsearch_assistant](https://github.com/sergio11/langgraph_jobsearch_assistant) — LangGraph state machine + PDF report output
- [jugallachhwani — Agentic AI Career Assistant](https://medium.com/@jugallachhwani15) — fan-out/fan-in parallelisation + centralised GraphState
- [vadim.blog — LangGraph Job Pre-Screening](https://vadim.blog/2026/01/25/langgraph-system-deepseek-powered-job-pre-screening-for-worldwide-remote-roles) — hybrid heuristic + LLM pre-filter pattern
- [kaifkohari10 — AI Job Hunt Agents](https://kaifkohari10.medium.com) — BaseAgent pattern + iterative refinement loops

## License

[MIT](LICENSE)
