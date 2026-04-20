import os
from datetime import datetime
from graph.state import GraphState

OUTPUT_DIR = "outputs"


def generate_report(state: GraphState) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    job = state.get("selected_job")
    cover = state.get("cover_letter")
    ats = state.get("ats_analysis")

    lines = [
        f"# HireIQ Report — {datetime.now().strftime('%B %d, %Y')}",
        "",
        f"## Role: {job.title} @ {job.company}" if job else "## Role: N/A",
        f"**Location:** {job.location}" if job else "",
        f"**Fit Score:** {job.fit_score}/10" if job else "",
        f"**Reasoning:** {job.reasoning}" if job else "",
        f"**URL:** {job.url}" if job else "",
        "",
    ]

    if cover:
        lines += ["## Cover Letter", "", cover.content, ""]

    if ats:
        lines += [
            "## ATS Keyword Analysis",
            "",
            f"**Missing keywords:** {', '.join(ats.missing_keywords)}",
            "",
            "**Where to add them:**",
        ]
        for s in ats.suggestions:
            lines.append(f"- {s}")
        lines.append("")

    md_content = "\n".join(lines)
    md_path = os.path.join(OUTPUT_DIR, f"report_{timestamp}.md")

    with open(md_path, "w") as f:
        f.write(md_content)

    try:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=11)
        for line in md_content.splitlines():
            clean = line.lstrip("#").strip()
            if not clean:
                pdf.ln(4)
            else:
                pdf.multi_cell(0, 6, clean)
        pdf_path = os.path.join(OUTPUT_DIR, f"report_{timestamp}.pdf")
        pdf.output(pdf_path)
        return pdf_path
    except ImportError:
        return md_path
