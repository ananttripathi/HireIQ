import gradio as gr
import os


def extract_resume_text(file_path: str) -> str:
    if not file_path:
        return ""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() or "" for page in reader.pages).strip()
    if ext in (".docx", ".doc"):
        from docx import Document
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs).strip()
    with open(file_path, "r", errors="ignore") as f:
        return f.read().strip()

# ── CSS ──────────────────────────────────────────────────────────────────────

CSS = """
/* ── Base ── */
.gradio-container {
  font-family: 'Inter', -apple-system, sans-serif !important;
  background: #0d0d0d !important;
  color: #e2e8f0 !important;
}
footer { display: none !important; }
.main { background: #0d0d0d !important; }

/* ── Header ── */
.hiq-header {
  background: linear-gradient(135deg, #0d0d0d 0%, #111827 60%, #1a1f35 100%);
  border: 1px solid #1e2a3a;
  border-radius: 16px; padding: 36px 40px; margin-bottom: 12px;
}
.hiq-header h1 { font-size: 2.4rem; font-weight: 800; margin: 0 0 6px 0;
  background: linear-gradient(90deg, #60a5fa, #a78bfa); -webkit-background-clip: text;
  -webkit-text-fill-color: transparent; letter-spacing: -1px; }
.hiq-header p  { font-size: 0.97rem; color: #64748b; margin: 0; }
.hiq-badge { display: inline-block; background: #1e293b; border: 1px solid #334155;
  border-radius: 20px; padding: 4px 12px; font-size: 0.77rem; margin: 12px 4px 0 0; color: #94a3b8; }

/* ── Tabs ── */
.tab-header { background: #111827 !important; border-bottom: 1px solid #1e293b !important; }
.tab-button { color: #64748b !important; font-size: 0.92rem !important;
  font-weight: 500 !important; padding: 10px 22px !important;
  background: transparent !important; border: none !important;
  border-radius: 0 !important; cursor: pointer !important;
  pointer-events: all !important; }
.tab-button.selected { color: #60a5fa !important; font-weight: 700 !important;
  border-bottom: 2px solid #60a5fa !important; }

/* ── Inputs ── */
textarea, input[type=text] {
  background: #111827 !important; border: 1.5px solid #1e293b !important;
  border-radius: 10px !important; color: #e2e8f0 !important; font-size: 0.93rem !important;
}
textarea:focus, input[type=text]:focus {
  border-color: #3b82f6 !important;
  box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
}
label span { color: #94a3b8 !important; font-weight: 600 !important; font-size: 0.85rem !important; }
.wrap { background: #0d0d0d !important; }

/* ── Buttons ── */
.btn-primary {
  background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
  color: white !important; border: none !important; border-radius: 10px !important;
  font-weight: 700 !important; font-size: 0.97rem !important;
  cursor: pointer !important; transition: all 0.2s !important;
  box-shadow: 0 4px 20px rgba(99,102,241,0.35) !important;
}
.btn-primary:hover { transform: translateY(-1px) !important;
  box-shadow: 0 6px 28px rgba(99,102,241,0.5) !important; }

/* ── Job cards ── */
.results-wrap { max-height: 640px; overflow-y: auto; padding-right: 6px; }
.job-card {
  background: #111827; border-radius: 14px; padding: 20px 22px; margin-bottom: 12px;
  border: 1px solid #1e293b; transition: border-color 0.2s, box-shadow 0.2s;
}
.job-card:hover { border-color: #3b82f6; box-shadow: 0 0 0 1px #3b82f633; }
.job-header { display: flex; align-items: flex-start; gap: 14px; }
.job-body   { flex: 1; }
.job-title  { font-size: 1rem; font-weight: 700; color: #f1f5f9; margin: 0 0 4px 0; }
.job-meta   { font-size: 0.85rem; color: #475569; margin: 0 0 8px 0; }
.job-reason { font-size: 0.88rem; color: #94a3b8; line-height: 1.55; margin: 8px 0 10px 0; }
.score-badge { display: inline-flex; align-items: center; justify-content: center;
  width: 46px; height: 46px; border-radius: 50%; font-weight: 800;
  font-size: 1rem; flex-shrink: 0; margin-top: 2px; }
.score-high { background: #052e16; color: #4ade80; border: 1.5px solid #166534; }
.score-mid  { background: #1c1400; color: #facc15; border: 1.5px solid #854d0e; }
.score-low  { background: #1f0707; color: #f87171; border: 1.5px solid #991b1b; }
.apply-btn  { display: inline-block; padding: 5px 14px;
  background: linear-gradient(135deg, #1d4ed8, #6d28d9);
  color: white !important; border-radius: 7px; font-size: 0.82rem;
  font-weight: 600; text-decoration: none; }
.salary-tag { display: inline-block; background: #0f172a; color: #60a5fa;
  border: 1px solid #1e3a5f; border-radius: 5px;
  padding: 2px 8px; font-size: 0.79rem; font-weight: 600; margin-left: 8px; }

/* ── Info pills ── */
.info-strip { display: flex; gap: 10px; flex-wrap: wrap; margin: 12px 0 4px 0; }
.info-pill  { background: #111827; border: 1px solid #1e293b; border-radius: 8px;
  padding: 8px 14px; font-size: 0.85rem; color: #cbd5e1; flex: 1; min-width: 140px; }
.info-pill strong { display: block; font-size: 0.72rem; color: #475569;
  text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 3px; }

/* ── ATS ── */
.ats-section { background: #111827; border-radius: 14px; padding: 20px 22px;
  border: 1px solid #1e293b; }
.keyword-chip { display: inline-block; border-radius: 6px; padding: 3px 10px;
  font-size: 0.81rem; font-weight: 600; margin: 3px; }
.chip-missing { background: #1f0707; color: #f87171; border: 1px solid #7f1d1d; }
.chip-present { background: #052e16; color: #4ade80; border: 1px solid #14532d; }
.section-label { font-size: 0.75rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.08em; color: #475569; margin: 16px 0 8px 0; }

/* ── Cover letter output ── */
#cover-out textarea {
  background: #0d1117 !important;
  border: 1px solid #1e293b !important;
  border-radius: 12px !important;
  color: #e2e8f0 !important;
  font-family: 'Georgia', serif !important;
  font-size: 0.93rem !important;
  line-height: 1.7 !important;
  padding: 16px !important;
}
#cover-out textarea:focus {
  border-color: #3b82f6 !important;
}

/* ── Output divider ── */
.output-divider {
  display: flex; align-items: center; gap: 12px;
  margin: 20px 0 12px 0;
}
.output-divider span {
  font-size: 0.75rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.1em; color: #334155; white-space: nowrap;
}
.output-divider::before, .output-divider::after {
  content: ""; flex: 1; height: 1px; background: #1e293b;
}

/* ── ATS empty state ── */
.ats-empty {
  background: #111827; border-radius: 12px; border: 1px dashed #1e293b;
  padding: 32px 20px; text-align: center;
  color: #334155; font-size: 0.9rem; font-style: italic;
}

/* ── Tracker ── */
.tracker-header {
  background: #111827; border: 1px solid #1e293b;
  border-radius: 12px; padding: 16px 20px; margin-bottom: 14px;
}
.refresh-btn {
  background: #1e293b !important; color: #94a3b8 !important;
  border: 1px solid #334155 !important; border-radius: 8px !important;
  font-size: 0.85rem !important; margin-bottom: 10px !important;
}
.refresh-btn:hover { background: #334155 !important; color: #e2e8f0 !important; }
#tracker-table {
  border-radius: 12px !important; overflow: hidden !important;
  border: 1px solid #1e293b !important;
}
#tracker-table table { background: #111827 !important; }
#tracker-table th {
  background: #0d1117 !important; color: #64748b !important;
  font-size: 0.78rem !important; text-transform: uppercase !important;
  letter-spacing: 0.06em !important; border-bottom: 1px solid #1e293b !important;
  padding: 10px 14px !important;
}
#tracker-table td {
  background: #111827 !important; color: #cbd5e1 !important;
  border-bottom: 1px solid #1a2332 !important;
  font-size: 0.88rem !important; padding: 10px 14px !important;
}
#tracker-table tr:hover td { background: #0d1f3c !important; }

/* ── File upload drop zone ── */
#resume-upload, #cl-upload {
  border: 2px dashed #2563eb !important;
  border-radius: 12px !important;
  background: #080f1e !important;
  transition: border-color 0.2s, background 0.2s !important;
  padding: 4px !important;
}
#resume-upload:hover, #cl-upload:hover {
  border-color: #60a5fa !important;
  background: #0d1f3c !important;
}
#resume-upload .wrap, #cl-upload .wrap,
#resume-upload > div, #cl-upload > div {
  background: transparent !important;
}
#resume-upload svg, #cl-upload svg {
  stroke: #3b82f6 !important;
  color: #3b82f6 !important;
  fill: none !important;
}
#resume-upload p, #cl-upload p,
#resume-upload span:not(.svelte-1oa8sb9),
#cl-upload span:not(.svelte-1oa8sb9) {
  color: #60a5fa !important;
}
#resume-upload button, #cl-upload button {
  background: #1e3a5f !important;
  color: #93c5fd !important;
  border: 1px solid #2563eb !important;
  border-radius: 8px !important;
  font-weight: 600 !important;
  margin-top: 6px !important;
}
#resume-upload button:hover, #cl-upload button:hover {
  background: #2563eb !important;
  color: white !important;
}
"""

# ── Stub data ─────────────────────────────────────────────────────────────────

SAMPLE_JOBS_HTML = """
<div class="results-wrap">

  <div class="job-card">
    <div class="job-header">
      <div class="job-body">
        <p class="job-title">Senior Machine Learning Engineer <span class="salary-tag">$180k – $220k</span></p>
        <p class="job-meta">Stripe &nbsp;·&nbsp; Remote, USA &nbsp;·&nbsp; via LinkedIn</p>
        <p class="job-reason">Strong Python + ML background matches core requirements. Prior fintech exposure is a plus. Stack alignment with PyTorch and MLflow is excellent.</p>
        <a class="apply-btn" href="https://stripe.com/jobs" target="_blank">View & Apply →</a>
      </div>
      <div class="score-badge score-high">9</div>
    </div>
  </div>

  <div class="job-card">
    <div class="job-header">
      <div class="job-body">
        <p class="job-title">ML Engineer — Recommendations @ Airbnb</p>
        <p class="job-meta">Airbnb &nbsp;·&nbsp; San Francisco, CA &nbsp;·&nbsp; via Indeed</p>
        <p class="job-reason">Solid ranking and recommendation systems experience. Missing Spark at scale — worth adding to resume before applying.</p>
        <a class="apply-btn" href="https://airbnb.com/careers" target="_blank">View & Apply →</a>
      </div>
      <div class="score-badge score-high">8</div>
    </div>
  </div>

  <div class="job-card">
    <div class="job-header">
      <div class="job-body">
        <p class="job-title">Staff Data Scientist <span class="salary-tag">$160k – $200k</span></p>
        <p class="job-meta">Notion &nbsp;·&nbsp; Remote &nbsp;·&nbsp; via Wellfound</p>
        <p class="job-reason">Good fit for product analytics focus. LLM work is a strong differentiator here.</p>
        <a class="apply-btn" href="https://notion.so/careers" target="_blank">View & Apply →</a>
      </div>
      <div class="score-badge score-mid">7</div>
    </div>
  </div>

  <div class="job-card">
    <div class="job-header">
      <div class="job-body">
        <p class="job-title">Machine Learning Engineer — Platform</p>
        <p class="job-meta">Figma &nbsp;·&nbsp; Remote, USA &nbsp;·&nbsp; via Greenhouse</p>
        <p class="job-reason">Platform ML role — infrastructure heavy. Kubernetes experience gap may be a concern.</p>
        <a class="apply-btn" href="https://figma.com/careers" target="_blank">View & Apply →</a>
      </div>
      <div class="score-badge score-mid">6</div>
    </div>
  </div>

</div>
"""

PROFILE_HTML = """
<div class="info-strip">
  <div class="info-pill"><strong>Seniority</strong>Senior</div>
  <div class="info-pill"><strong>Experience</strong>6 years</div>
  <div class="info-pill"><strong>Top Skills</strong>Python · PyTorch · SQL · MLflow · LLMs</div>
  <div class="info-pill"><strong>Pipeline</strong>42 fetched → 18 filtered → 10 scored</div>
</div>
"""

SAMPLE_COVER = """Dear Hiring Team at Stripe,

I'm excited to apply for the Senior Machine Learning Engineer role. Having spent six years building and shipping ML systems — from recommendation engines to real-time fraud models — I'm drawn to Stripe's commitment to using ML as a core product differentiator rather than an afterthought.

At my last role, I led a team that reduced model inference latency by 40% while improving precision by 12 points. I've worked extensively with PyTorch, MLflow, and distributed training on GPU clusters, which aligns directly with your infrastructure requirements.

I'd welcome the opportunity to discuss how my background fits the team's goals.

Best regards,
Anant Tripathi"""

SAMPLE_ATS_HTML = """
<div class="ats-section">
  <p class="section-label">Missing — add these to your resume</p>
  <span class="keyword-chip chip-missing">Kafka</span>
  <span class="keyword-chip chip-missing">Flink</span>
  <span class="keyword-chip chip-missing">feature store</span>
  <span class="keyword-chip chip-missing">A/B testing at scale</span>
  <span class="keyword-chip chip-missing">model monitoring</span>

  <p class="section-label" style="margin-top:16px">Already present — you're covered</p>
  <span class="keyword-chip chip-present">Python</span>
  <span class="keyword-chip chip-present">PyTorch</span>
  <span class="keyword-chip chip-present">MLflow</span>
  <span class="keyword-chip chip-present">SQL</span>
  <span class="keyword-chip chip-present">distributed training</span>

  <p class="section-label" style="margin-top:16px">Where to add missing keywords</p>
  <ul style="font-size:0.9rem; color:#94a3b8; line-height:1.8; padding-left:18px; margin:0;">
    <li>Add <strong>Kafka</strong> and <strong>Flink</strong> to your data pipeline bullet at Company X</li>
    <li>Mention <strong>A/B testing at scale</strong> in your recommendation system project</li>
    <li>Add <strong>feature store</strong> to your ML infrastructure section</li>
    <li>Add a one-liner on <strong>model monitoring</strong> to your MLOps experience</li>
  </ul>
</div>
"""

# ── Stub handlers ─────────────────────────────────────────────────────────────

def run_search(resume_text, search_query, progress=gr.Progress()):
    if not resume_text.strip():
        return "<p style='color:#991b1b;padding:16px'>Please paste your resume.</p>", ""
    if not search_query.strip():
        return "<p style='color:#991b1b;padding:16px'>Please enter a search query.</p>", ""
    progress(0.25, desc="Parsing resume...")
    progress(0.55, desc="Fetching live jobs...")
    progress(0.85, desc="Scoring with LLM...")
    return SAMPLE_JOBS_HTML, PROFILE_HTML


def run_cover_ats(resume_text, job_title, company, job_description, url, progress=gr.Progress()):
    if not resume_text.strip() or not job_title.strip():
        return "Missing resume or job title.", ""
    progress(0.4, desc="Writing cover letter...")
    progress(0.8, desc="Running ATS analysis...")
    return SAMPLE_COVER, SAMPLE_ATS_HTML


def load_tracker():
    try:
        from tools.tracker import load_applications
        rows = load_applications()
        return [[r.get("date"), r.get("title"), r.get("company"),
                 r.get("location"), r.get("fit_score"), r.get("url")] for r in rows]
    except Exception:
        return []


# ── Layout ────────────────────────────────────────────────────────────────────

with gr.Blocks(title="HireIQ") as demo:

    gr.HTML("""
    <div class="hiq-header">
      <h1>🎯 HireIQ</h1>
      <p>Agentic job hunting assistant — finds, scores, and helps you apply to the right roles</p>
      <span class="hiq-badge">Groq LLaMA 3.3 70B</span>
      <span class="hiq-badge">DuckDuckGo Search</span>
      <span class="hiq-badge">Adzuna API</span>
      <span class="hiq-badge">LangGraph</span>
      <span class="hiq-badge">100% Free · No credit card</span>
    </div>
    """)

    with gr.Tab("🔍  Search & Score"):

        with gr.Row(equal_height=False):
            with gr.Column(scale=5):
                resume_upload = gr.File(
                    label="Upload Resume (PDF, DOCX, or TXT)",
                    file_types=[".pdf", ".docx", ".doc", ".txt"],
                    type="filepath",
                    elem_id="resume-upload",
                )
                resume_input = gr.Textbox(
                    label="Resume text (auto-filled on upload, or paste directly)",
                    placeholder="Upload a file above, or paste your resume here…",
                    lines=16,
                )
                resume_upload.change(
                    fn=extract_resume_text,
                    inputs=resume_upload,
                    outputs=resume_input,
                )
            with gr.Column(scale=3):
                search_input = gr.Textbox(
                    label="Search Query",
                    placeholder="e.g.  Senior ML Engineer remote\n      Python Backend Engineer NYC",
                    lines=3,
                )
                search_btn = gr.Button("Find & Score Jobs →", variant="primary", elem_classes="btn-primary")
                profile_out = gr.HTML()

        results_out = gr.HTML()

        search_btn.click(
            fn=run_search,
            inputs=[resume_input, search_input],
            outputs=[results_out, profile_out],
        )

    with gr.Tab("✉️  Cover Letter & ATS"):

        gr.HTML('<p style="color:#64748b;font-size:0.9rem;margin:2px 0 14px 0">Pick a role from the search results (or any job you want) and generate a personalised cover letter + ATS keyword gap analysis.</p>')

        with gr.Row(equal_height=False):
            with gr.Column(scale=5):
                cl_upload = gr.File(
                    label="Upload Resume (PDF, DOCX, or TXT)",
                    file_types=[".pdf", ".docx", ".doc", ".txt"],
                    type="filepath",
                    elem_id="cl-upload",
                )
                cl_resume = gr.Textbox(
                    label="Resume text (auto-filled on upload, or paste directly)",
                    placeholder="Upload a file above, or paste your resume here…",
                    lines=8,
                )
                cl_upload.change(fn=extract_resume_text, inputs=cl_upload, outputs=cl_resume)
                cl_description = gr.Textbox(
                    label="Job Description",
                    placeholder="Paste the full job description here…",
                    lines=7,
                )
            with gr.Column(scale=3):
                cl_title   = gr.Textbox(label="Job Title",  placeholder="e.g.  Senior ML Engineer")
                cl_company = gr.Textbox(label="Company",    placeholder="e.g.  Stripe")
                cl_url     = gr.Textbox(label="Job URL",    placeholder="https://…")
                cl_btn = gr.Button("Generate Cover Letter + ATS →", variant="primary", elem_classes="btn-primary")

        gr.HTML('<div class="output-divider"><span>Generated Output</span></div>')

        with gr.Row(equal_height=False):
            with gr.Column(scale=1):
                gr.HTML('<p class="section-label">Cover Letter</p>')
                cover_out = gr.Textbox(
                    lines=18, show_label=False, interactive=True,
                    placeholder="Your cover letter will appear here — fully editable before you copy it.",
                    elem_id="cover-out",
                )
            with gr.Column(scale=1):
                gr.HTML('<p class="section-label">ATS Keyword Gap</p>')
                ats_out = gr.HTML(
                    value='<div class="ats-empty">Run the generator to see which keywords you\'re missing.</div>'
                )

        cl_btn.click(
            fn=run_cover_ats,
            inputs=[cl_resume, cl_title, cl_company, cl_description, cl_url],
            outputs=[cover_out, ats_out],
        )

    with gr.Tab("📋  Application Tracker"):
        gr.HTML("""
        <div class="tracker-header">
          <div>
            <h3 style="margin:0 0 4px 0;color:#f1f5f9;font-size:1.1rem;font-weight:700">Application Pipeline</h3>
            <p style="margin:0;color:#64748b;font-size:0.88rem">Every role you generate a cover letter for is logged here automatically.</p>
          </div>
        </div>
        """)
        refresh_btn = gr.Button("↻  Refresh", size="sm", elem_classes="refresh-btn")
        tracker_table = gr.Dataframe(
            headers=["Date", "Title", "Company", "Location", "Fit Score", "URL"],
            datatype=["str", "str", "str", "str", "number", "str"],
            interactive=False,
            wrap=True,
            elem_id="tracker-table",
        )
        refresh_btn.click(fn=load_tracker, outputs=tracker_table)
        demo.load(fn=load_tracker, outputs=tracker_table)

if __name__ == "__main__":
    demo.launch(css=CSS, theme=gr.themes.Base(
        primary_hue=gr.themes.colors.blue,
        neutral_hue=gr.themes.colors.slate,
    ))
