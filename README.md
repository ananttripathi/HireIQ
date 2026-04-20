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

HireIQ is a multi-agent AI system that automates the most painful parts of job hunting. Give it your resume and a job search query, and a team of specialised agents will find relevant roles, score them against your profile, tailor your resume, and write personalised cover letters — in under 2 minutes.

## The Problem

Job hunting is exhausting and repetitive. Senior engineers spend hours:
- Searching across LinkedIn, Indeed, Wellfound, and company career pages separately
- Manually tailoring resumes for each role
- Writing cover letters from scratch
- Tracking applications with no structure
- Guessing whether their resume will pass ATS filters

## The Solution

A crew of AI agents that collaborates end-to-end:

```
User Input: "Senior ML Engineer roles in Bengaluru, remote-friendly, fintech or pharma"
        |
        v
Search Agent       Searches LinkedIn, Indeed, Wellfound via Serper API
        |
        v
Screening Agent    Scores each role against your resume and preferences
        |
        v
Resume Agent       Tailors resume bullets for top matching roles
        |
        v
Cover Letter Agent Writes a personalised cover letter per role
        |
        v
Output: Ranked job list + tailored resume + cover letter ready to send
```

## Features

- Multi-board job search (LinkedIn, Indeed, Wellfound, Google Jobs)
- Resume-to-job fit scoring with reasoning
- Automated resume tailoring per role
- Personalised cover letter generation
- Clean Gradio UI deployable on Hugging Face Spaces

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent orchestration | CrewAI |
| LLM | Groq (LLaMA 3.3 70B) — free |
| Job search | Serper API — free tier |
| UI | Gradio |
| Deployment | Hugging Face Spaces + GitHub Actions |

## Project Structure

```
HireIQ/
├── app.py                  # Gradio UI + agent pipeline entry point
├── agents/
│   ├── search_agent.py     # Finds job listings via Serper
│   ├── screening_agent.py  # Scores roles against user resume
│   ├── resume_agent.py     # Tailors resume bullets per role
│   └── cover_letter_agent.py  # Generates personalised cover letters
├── tools/
│   ├── serper_tool.py      # Serper API wrapper for job search
│   └── resume_parser.py    # Extracts structured data from resume
├── outputs/                # Generated resumes and cover letters
├── requirements.txt
└── .github/
    └── workflows/
        └── deploy-hf.yml   # Auto-deploy to HF Spaces on push
```

## Setup

```bash
git clone https://github.com/ananttripathi/HireIQ.git
cd HireIQ
pip install -r requirements.txt
```

Set the following environment variables:

```bash
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
```

Get free API keys:
- Groq: https://console.groq.com
- Serper: https://serper.dev (free tier: 2,500 searches/month)

## Deploy to Hugging Face Spaces

1. Create a new Gradio Space at huggingface.co
2. Push this repo to the Space
3. Add `GROQ_API_KEY` and `SERPER_API_KEY` as Space secrets

GitHub Actions auto-deploys on every push to `main` — add `HF_TOKEN` as a GitHub repo secret.

## License

[MIT](LICENSE)
