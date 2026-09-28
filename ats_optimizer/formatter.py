"""Formatted output generator for ATS Resumes: Markdown, ATS-compliant HTML, and JSON reports.

Enforces strict structural preservation:
  - Uses original section headers verbatim (never renames them).
  - Preserves original company names, job titles, dates, locations.
  - Only replaces experience bullet points with XYZ-rewritten versions.
  - Renders non-experience sections (education, skills, projects) verbatim.
"""

from __future__ import annotations

import json
from html import escape
from typing import Any

from .ats_matcher import ATSOptimizationReport
from .parser import ParsedResume, parse_resume_full, parse_resume_structure


def format_markdown_resume(
    report: ATSOptimizationReport,
    original_resume_text: str
) -> str:
    """Generates a clean, ATS-compliant Markdown resume preserving the original structure.
    
    Rules:
      - Section headers from the original resume are used verbatim.
      - Company names, job titles, dates, locations are preserved exactly.
      - Only bullet points under experience sections are replaced.
      - Non-experience sections are rendered as-is.
    """
    parsed = parse_resume_full(original_resume_text)
    name = parsed.name or "CANDIDATE"
    contacts = " | ".join(parsed.contact_lines) or ""

    md = []
    md.append(f"# {name}")
    if contacts:
        md.append(f"**{contacts}**\n")
    md.append("---\n")

    bullet_idx = 0  # Track which rewritten bullet to use

    for section in parsed.sections:
        if section.section_type == "preamble":
            # Lines before first section header (rare)
            for ln in section.content_lines:
                if ln.strip():
                    md.append(ln.strip())
            md.append("")
            continue

        # Use the ORIGINAL section header — never rename
        md.append(f"## {section.header}")

        if section.section_type == "experience":
            # Render each experience block with original metadata
            for exp in parsed.experiences:
                # Render original role header (title + company + dates)
                header_parts = []
                if exp.title:
                    header_parts.append(f"**{exp.title}**")
                if exp.company:
                    header_parts.append(f"*{exp.company}*")
                if exp.dates:
                    header_parts.append(f"({exp.dates})")
                if exp.location:
                    header_parts.append(f"— {exp.location}")
                
                if header_parts:
                    md.append(f"### {' | '.join(header_parts)}")
                elif exp.header_line:
                    md.append(f"### {exp.header_line}")

                md.append("")

                # Replace bullets with XYZ-rewritten versions (if available)
                for _ in exp.bullets:
                    if bullet_idx < len(report.optimized_bullets):
                        b = report.optimized_bullets[bullet_idx]
                        md.append(f"- {b.rewritten}")
                        if b.keywords_infused:
                            md.append(f"  *(Keywords infused: {', '.join(b.keywords_infused)})*")
                        bullet_idx += 1
                    else:
                        # Fallback: if we ran out of rewritten bullets, use original
                        md.append(f"- {exp.bullets[bullet_idx - len(report.optimized_bullets)] if bullet_idx < len(exp.bullets) + len(report.optimized_bullets) else ''}")
                md.append("")

        elif section.section_type == "skills":
            # Merge original skills with optimized matrix
            # First render original content
            for ln in section.content_lines:
                if ln.strip():
                    md.append(ln.strip())
            # Then append any additional skills from the optimization
            added_skills = False
            for category, skills in report.optimized_skills_matrix.items():
                if skills:
                    # Check if these skills are already mentioned
                    existing_text = "\n".join(section.content_lines).lower()
                    new_skills = [s for s in skills if s.lower() not in existing_text]
                    if new_skills:
                        if not added_skills:
                            md.append("")
                            md.append("**Additional ATS-Optimized Skills:**")
                            added_skills = True
                        md.append(f"- **{category}:** {', '.join(new_skills)}")
            md.append("")

        else:
            # All other sections (education, projects, summary, etc.) — render verbatim
            for ln in section.content_lines:
                if ln.strip():
                    md.append(ln.strip())
            md.append("")

    return "\n".join(md)


def format_html_resume(
    report: ATSOptimizationReport,
    original_resume_text: str
) -> str:
    """Generates an ATS-compliant, single-column HTML resume preserving original structure.
    
    Rules:
      - Section headers from the original resume are used verbatim.
      - Company names, job titles, dates, locations are preserved exactly.
      - Only bullet points under experience sections are replaced.
    """
    parsed = parse_resume_full(original_resume_text)
    name = escape(parsed.name or "CANDIDATE")
    contacts = escape(" | ".join(parsed.contact_lines) or "")

    bullet_idx = 0
    sections_html = ""

    for section in parsed.sections:
        if section.section_type == "preamble":
            content = "<br>".join(escape(ln.strip()) for ln in section.content_lines if ln.strip())
            sections_html += f"<p class=\"summary-text\">{content}</p>\n"
            continue

        # Original header — verbatim
        header_esc = escape(section.header)
        sections_html += f"<section>\n<h2>{header_esc}</h2>\n"

        if section.section_type == "experience":
            for exp in parsed.experiences:
                # Original metadata — verbatim
                title_esc = escape(exp.title) if exp.title else ""
                company_esc = escape(exp.company) if exp.company else ""
                dates_esc = escape(exp.dates) if exp.dates else ""
                location_esc = escape(exp.location) if exp.location else ""

                if title_esc or company_esc or dates_esc:
                    sections_html += "<div class=\"job-header\">\n"
                    left_parts = [p for p in [title_esc, company_esc] if p]
                    sections_html += f"<span>{' | '.join(left_parts)}</span>\n"
                    right_parts = [p for p in [dates_esc, location_esc] if p]
                    sections_html += f"<span>{' | '.join(right_parts)}</span>\n"
                    sections_html += "</div>\n"
                elif exp.header_line:
                    sections_html += f"<div class=\"job-header\"><span>{escape(exp.header_line)}</span></div>\n"

                sections_html += "<ul class=\"experience-list\">\n"
                for _ in exp.bullets:
                    if bullet_idx < len(report.optimized_bullets):
                        b = report.optimized_bullets[bullet_idx]
                        bullet_esc = escape(b.rewritten)
                        infused_html = ""
                        if b.keywords_infused:
                            infused_badges = " ".join(f'<span class="kw-tag">{escape(k)}</span>' for k in b.keywords_infused)
                            infused_html = f'<div class="kw-container"><small>Infused Keywords:</small> {infused_badges}</div>'
                        sections_html += f"<li class=\"bullet-item\"><div class=\"bullet-text\">{bullet_esc}</div>{infused_html}</li>\n"
                        bullet_idx += 1
                sections_html += "</ul>\n"

        elif section.section_type == "skills":
            # Render original skills verbatim
            sections_html += "<ul class=\"skills-list\">\n"
            for ln in section.content_lines:
                stripped = ln.strip()
                if stripped:
                    sections_html += f"<li>{escape(stripped)}</li>\n"
            # Append optimized skills
            existing_text = "\n".join(section.content_lines).lower()
            for category, skills in report.optimized_skills_matrix.items():
                new_skills = [s for s in skills if s.lower() not in existing_text]
                if new_skills:
                    cat_esc = escape(category)
                    skills_esc = escape(", ".join(new_skills))
                    sections_html += f"<li><strong>{cat_esc} (ATS-Optimized):</strong> {skills_esc}</li>\n"
            sections_html += "</ul>\n"

        else:
            # All other sections — render verbatim
            for ln in section.content_lines:
                stripped = ln.strip()
                if stripped:
                    is_bullet = stripped.startswith(("-", "*", "•"))
                    if is_bullet:
                        clean = stripped.lstrip("-*• ").strip()
                        sections_html += f"<li>{escape(clean)}</li>\n"
                    else:
                        sections_html += f"<p class=\"summary-text\">{escape(stripped)}</p>\n"

        sections_html += "</section>\n"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} — ATS-Optimized Resume</title>
<style>
    @page {{
        margin: 0.6in;
        size: letter;
    }}
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        line-height: 1.5;
        color: #1a1a1a;
        background-color: #ffffff;
        margin: 0;
        padding: 40px;
    }}
    .resume-container {{
        max-width: 800px;
        margin: 0 auto;
        background: #fff;
    }}
    header {{
        text-align: center;
        border-bottom: 2px solid #2563eb;
        padding-bottom: 12px;
        margin-bottom: 20px;
    }}
    h1 {{
        font-size: 26px;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin: 0 0 6px 0;
        color: #0f172a;
    }}
    .contact-info {{
        font-size: 13px;
        color: #475569;
    }}
    section {{
        margin-bottom: 18px;
    }}
    h2 {{
        font-size: 15px;
        text-transform: uppercase;
        color: #1e3a8a;
        border-bottom: 1px solid #cbd5e1;
        padding-bottom: 4px;
        margin: 16px 0 10px 0;
        letter-spacing: 0.5px;
    }}
    .summary-text {{
        font-size: 13.5px;
        color: #334155;
        text-align: justify;
    }}
    ul.skills-list {{
        list-style: none;
        padding: 0;
        margin: 0;
        font-size: 13px;
    }}
    ul.skills-list li {{
        margin-bottom: 4px;
    }}
    .job-header {{
        display: flex;
        justify-content: space-between;
        font-size: 14px;
        font-weight: bold;
        color: #0f172a;
    }}
    .job-sub {{
        font-size: 13px;
        color: #64748b;
        font-style: italic;
        margin-bottom: 8px;
    }}
    ul.experience-list {{
        padding-left: 20px;
        margin: 0;
    }}
    .bullet-item {{
        margin-bottom: 10px;
        font-size: 13px;
        color: #1e293b;
    }}
    .kw-container {{
        margin-top: 3px;
    }}
    .kw-tag {{
        display: inline-block;
        background: #eff6ff;
        color: #1d4ed8;
        border: 1px solid #bfdbfe;
        font-size: 11px;
        padding: 1px 6px;
        border-radius: 4px;
        font-weight: 500;
        margin-right: 4px;
    }}
    @media print {{
        body {{
            padding: 0;
        }}
        .kw-container {{
            display: none !important;
        }}
    }}
</style>
</head>
<body>
<div class="resume-container">
    <header>
        <h1>{name}</h1>
        <div class="contact-info">{contacts}</div>
    </header>

    {sections_html}
</div>
</body>
</html>
"""
    return html


def format_xyz_bullet_table_markdown(report: ATSOptimizationReport) -> str:
    """Creates a Markdown comparison table showing original vs XYZ rewritten bullets."""
    lines = [
        "| # | Original Bullet | Google XYZ Rewritten Bullet | Infused Keywords |",
        "|---|---|---|---|",
    ]
    for i, b in enumerate(report.optimized_bullets, 1):
        orig_clean = b.original.replace("|", "\\|").replace("\n", " ")
        rewr_clean = b.rewritten.replace("|", "\\|").replace("\n", " ")
        kws = ", ".join(b.keywords_infused) if b.keywords_infused else "—"
        lines.append(f"| {i} | {orig_clean} | **{rewr_clean}** | `{kws}` |")
    return "\n".join(lines)


def format_analysis_summary_markdown(report: ATSOptimizationReport) -> str:
    """Generates an executive analysis markdown report detailing ATS keyword scores and XYZ impact."""
    status_badge = "✅ PASSED (>= 90%)" if report.passed_90 else "⚠️ IN PROGRESS"
    
    md = [
        f"## 🎯 ATS Keyword Match & Google XYZ Optimization Audit",
        f"",
        f"- **Initial Match Score:** `{report.initial_score:.1f}%`",
        f"- **Post-XYZ Rewriting Score:** `{report.post_rewrite_score:.1f}%`",
        f"- **Final Optimized Score:** **`{report.final_score:.1f}%`**",
        f"- **90%+ ATS Target Threshold:** **{status_badge}**",
        f"- **Optimization Iterations:** `{report.iterations_run}`",
        f"- **Page Budget:** `{report.original_page_count} page(s)` (estimated output: `{report.estimated_output_pages}`)",
        f"- **Max Bullet Words:** `{report.max_bullet_words}`",
        f"",
        f"### 📊 Keyword Coverage Metrics",
        f"- **Initial Matched Keywords ({len(report.initial_matched_keywords)}):** {', '.join(f'`{k}`' for k in report.initial_matched_keywords) or 'None'}",
        f"- **Initial Missing Keywords ({len(report.initial_missing_keywords)}):** {', '.join(f'`{k}`' for k in report.initial_missing_keywords) or 'None'}",
        f"- **Final Keyword Coverage ({len(report.post_rewrite_matched)}):** {', '.join(f'`{k}`' for k in report.post_rewrite_matched)}",
        f"",
        f"### ⚙️ Optimization Audit Trail",
    ]
    for note in report.optimization_notes:
        md.append(f"- {note}")

    return "\n".join(md)
