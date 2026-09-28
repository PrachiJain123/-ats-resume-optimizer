"""Formatted output generator for ATS Resumes: Markdown, ATS-compliant HTML, and JSON reports.

Enforces strict structural preservation:
 &bull; - Uses original section headers verbatim (never renames them).
 &bull; - Preserves original company names, job titles, dates, locations.
 &bull; - Only replaces experience bullet points with XYZ-rewritten versions.
 &bull; - Renders non-experience sections (education, skills, projects) verbatim.
"""

from __future__ import annotations

import json
from html import escape
from typing import Any

from .ats_matcher import ATSOptimizationReport
from .parser import ParsedResume, parse_resume_full, parse_resume_structure


def format_markdown_resume(
 &bull;  &bull; report: ATSOptimizationReport,
 &bull;  &bull; original_resume_text: str
) -> str:
 &bull;  &bull; """Generates a clean, ATS-compliant Markdown resume preserving the original structure.
 &bull;  &bull; 
 &bull;  &bull; Rules:
 &bull;  &bull;  &bull; - Section headers from the original resume are used verbatim.
 &bull;  &bull;  &bull; - Company names, job titles, dates, locations are preserved exactly.
 &bull;  &bull;  &bull; - Only bullet points under experience sections are replaced.
 &bull;  &bull;  &bull; - Non-experience sections are rendered as-is.
 &bull;  &bull; """
 &bull;  &bull; parsed = parse_resume_full(original_resume_text)
 &bull;  &bull; name = "P R A C H I &bull;  J A I N"
 &bull;  &bull; contacts = "Hyderabad, India | +91-6266761271 | prachijain6699@gmail.com"
 &bull;  &bull; links = "LinkedIn: [linkedin.com/in/prachi-jain6584](https://linkedin.com/in/prachi-jain6584) &bull; GitHub: [github.com/PrachiJain123](https://github.com/PrachiJain123) &bull; Portfolio: [https://prachijain123.github.io/](https://prachijain123.github.io/)"

 &bull;  &bull; md = []
 &bull;  &bull; md.append(f"# {name}")
 &bull;  &bull; md.append(f"{contacts}")
 &bull;  &bull; md.append(f"{links}")
 &bull;  &bull; md.append("**Immediate Joiner**\n")
 &bull;  &bull; md.append("---\n")

 &bull;  &bull; bullet_idx = 0 &bull; # Track which rewritten bullet to use

 &bull;  &bull; for section in parsed.sections:
 &bull;  &bull;  &bull;  &bull; if section.section_type == "preamble":
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; # Lines before first section header (rare)
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; for ln in section.content_lines:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; if ln.strip():
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; md.append(ln.strip())
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; md.append("")
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; continue

 &bull;  &bull;  &bull;  &bull; # Use the ORIGINAL section header — never rename
 &bull;  &bull;  &bull;  &bull; md.append(f"## {section.header}")

 &bull;  &bull;  &bull;  &bull; if section.section_type == "experience":
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; # Render each experience block with original metadata
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; for exp in parsed.experiences:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; # Render original role header (title + company + dates)
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; header_parts = []
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; if exp.title:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; header_parts.append(f"**{exp.title}**")
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; if exp.company:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; header_parts.append(f"*{exp.company}*")
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; if exp.dates:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; header_parts.append(f"({exp.dates})")
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; if exp.location:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; header_parts.append(f"— {exp.location}")
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; 
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; if header_parts:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; md.append(f"### {' | '.join(header_parts)}")
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; elif exp.header_line:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; md.append(f"### {exp.header_line}")

 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; md.append("")

 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; # Replace bullets with XYZ-rewritten versions (if available)
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; for _ in exp.bullets:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; if bullet_idx < len(report.optimized_bullets):
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; b = report.optimized_bullets[bullet_idx]
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; md.append(f"- {b.rewritten}")
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; if b.keywords_infused:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; md.append(f" &bull; *(Keywords infused: {', '.join(b.keywords_infused)})*")
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; bullet_idx += 1
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; else:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; # Fallback: if we ran out of rewritten bullets, use original
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; md.append(f"- {exp.bullets[bullet_idx - len(report.optimized_bullets)] if bullet_idx < len(exp.bullets) + len(report.optimized_bullets) else ''}")
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; md.append("")

 &bull;  &bull;  &bull;  &bull; elif section.section_type == "skills":
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; # Merge original skills with optimized matrix
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; # First render original content
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; for ln in section.content_lines:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; if ln.strip():
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; md.append(ln.strip())
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; # Then append any additional skills from the optimization
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; added_skills = False
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; for category, skills in report.optimized_skills_matrix.items():
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; if skills:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; # Check if these skills are already mentioned
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; existing_text = "\n".join(section.content_lines).lower()
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; new_skills = [s for s in skills if s.lower() not in existing_text]
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; if new_skills:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; if not added_skills:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; md.append("")
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; md.append("**Additional ATS-Optimized Skills:**")
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; added_skills = True
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; md.append(f"- **{category}:** {', '.join(new_skills)}")
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; md.append("")

 &bull;  &bull;  &bull;  &bull; else:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; # All other sections (education, projects, summary, etc.) — render verbatim
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; for ln in section.content_lines:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; if ln.strip():
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; md.append(ln.strip())
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; md.append("")

 &bull;  &bull; return "\n".join(md)


def format_html_resume(
 &bull;  &bull; report: ATSOptimizationReport,
 &bull;  &bull; original_resume_text: str
) -> str:
 &bull;  &bull; """Generates an ATS-compliant, single-column HTML resume preserving original structure.
 &bull;  &bull; 
 &bull;  &bull; Rules:
 &bull;  &bull;  &bull; - Section headers from the original resume are used verbatim.
 &bull;  &bull;  &bull; - Company names, job titles, dates, locations are preserved exactly.
 &bull;  &bull;  &bull; - Only bullet points under experience sections are replaced.
 &bull;  &bull; """
 &bull;  &bull; parsed = parse_resume_full(original_resume_text)
 &bull;  &bull; name = escape(parsed.name or "CANDIDATE")
 &bull;  &bull; contacts = escape(" | ".join(parsed.contact_lines) or "")

 &bull;  &bull; bullet_idx = 0
 &bull;  &bull; sections_html = ""

 &bull;  &bull; for section in parsed.sections:
 &bull;  &bull;  &bull;  &bull; if section.section_type == "preamble":
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; content = "<br>".join(escape(ln.strip()) for ln in section.content_lines if ln.strip())
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; sections_html += f"<p class=\"summary-text\">{content}</p>\n"
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; continue

 &bull;  &bull;  &bull;  &bull; # Original header — verbatim
 &bull;  &bull;  &bull;  &bull; header_esc = escape(section.header)
 &bull;  &bull;  &bull;  &bull; sections_html += f"<section>\n<h2>{header_esc}</h2>\n"

 &bull;  &bull;  &bull;  &bull; if section.section_type == "experience":
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; for exp in parsed.experiences:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; # Original metadata — verbatim
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; title_esc = escape(exp.title) if exp.title else ""
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; company_esc = escape(exp.company) if exp.company else ""
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; dates_esc = escape(exp.dates) if exp.dates else ""
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; location_esc = escape(exp.location) if exp.location else ""

 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; if title_esc or company_esc or dates_esc:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; sections_html += "<div class=\"job-header\">\n"
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; left_parts = [p for p in [title_esc, company_esc] if p]
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; sections_html += f"<span>{' | '.join(left_parts)}</span>\n"
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; right_parts = [p for p in [dates_esc, location_esc] if p]
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; sections_html += f"<span>{' | '.join(right_parts)}</span>\n"
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; sections_html += "</div>\n"
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; elif exp.header_line:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; sections_html += f"<div class=\"job-header\"><span>{escape(exp.header_line)}</span></div>\n"

 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; sections_html += "<ul class=\"experience-list\">\n"
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; for _ in exp.bullets:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; if bullet_idx < len(report.optimized_bullets):
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; b = report.optimized_bullets[bullet_idx]
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; bullet_esc = escape(b.rewritten)
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; infused_html = ""
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; if b.keywords_infused:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; infused_badges = " ".join(f'<span class="kw-tag">{escape(k)}</span>' for k in b.keywords_infused)
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; infused_html = f'<div class="kw-container"><small>Infused Keywords:</small> {infused_badges}</div>'
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; sections_html += f"<li class=\"bullet-item\"><div class=\"bullet-text\">{bullet_esc}</div>{infused_html}</li>\n"
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; bullet_idx += 1
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; sections_html += "</ul>\n"

 &bull;  &bull;  &bull;  &bull; elif section.section_type == "skills":
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; # Render original skills verbatim
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; sections_html += "<ul class=\"skills-list\">\n"
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; for ln in section.content_lines:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; stripped = ln.strip()
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; if stripped:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; sections_html += f"<li>{escape(stripped)}</li>\n"
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; # Append optimized skills
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; existing_text = "\n".join(section.content_lines).lower()
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; for category, skills in report.optimized_skills_matrix.items():
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; new_skills = [s for s in skills if s.lower() not in existing_text]
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; if new_skills:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; cat_esc = escape(category)
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; skills_esc = escape(", ".join(new_skills))
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; sections_html += f"<li><strong>{cat_esc} (ATS-Optimized):</strong> {skills_esc}</li>\n"
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; sections_html += "</ul>\n"

 &bull;  &bull;  &bull;  &bull; else:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; # All other sections — render verbatim
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; for ln in section.content_lines:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; stripped = ln.strip()
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; if stripped:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; is_bullet = stripped.startswith(("-", "*", "•"))
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; if is_bullet:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; clean = stripped.lstrip("-*• ").strip()
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; sections_html += f"<li>{escape(clean)}</li>\n"
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; else:
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull;  &bull; sections_html += f"<p class=\"summary-text\">{escape(stripped)}</p>\n"

 &bull;  &bull;  &bull;  &bull; sections_html += "</section>\n"

 &bull;  &bull; html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} — ATS-Optimized Resume</title>
<style>
 &bull;  &bull; @page {{
 &bull;  &bull;  &bull;  &bull; margin: 0.6in;
 &bull;  &bull;  &bull;  &bull; size: letter;
 &bull;  &bull; }}
 &bull;  &bull; body {{
 &bull;  &bull;  &bull;  &bull; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
 &bull;  &bull;  &bull;  &bull; line-height: 1.5;
 &bull;  &bull;  &bull;  &bull; color: #1a1a1a;
 &bull;  &bull;  &bull;  &bull; background-color: #ffffff;
 &bull;  &bull;  &bull;  &bull; margin: 0;
 &bull;  &bull;  &bull;  &bull; padding: 40px;
 &bull;  &bull; }}
 &bull;  &bull; .resume-container {{
 &bull;  &bull;  &bull;  &bull; max-width: 800px;
 &bull;  &bull;  &bull;  &bull; margin: 0 auto;
 &bull;  &bull;  &bull;  &bull; background: #fff;
 &bull;  &bull; }}
 &bull;  &bull; header {{
 &bull;  &bull;  &bull;  &bull; text-align: left;
 &bull;  &bull;  &bull;  &bull; border-bottom: 3px solid #d96b27;
 &bull;  &bull;  &bull;  &bull; padding-bottom: 8px;
 &bull;  &bull;  &bull;  &bull; margin-bottom: 18px;
 &bull;  &bull; }}
 &bull;  &bull; .resume-name {{
 &bull;  &bull;  &bull;  &bull; font-size: 20px;
 &bull;  &bull;  &bull;  &bull; font-weight: 800;
 &bull;  &bull;  &bull;  &bull; letter-spacing: 3px;
 &bull;  &bull;  &bull;  &bull; text-transform: uppercase;
 &bull;  &bull;  &bull;  &bull; color: #111827;
 &bull;  &bull;  &bull;  &bull; margin-bottom: 6px;
 &bull;  &bull; }}
 &bull;  &bull; .resume-contact-line {{
 &bull;  &bull;  &bull;  &bull; font-size: 13px;
 &bull;  &bull;  &bull;  &bull; color: #374151;
 &bull;  &bull;  &bull;  &bull; line-height: 1.5;
 &bull;  &bull;  &bull;  &bull; margin-bottom: 2px;
 &bull;  &bull; }}
 &bull;  &bull; .resume-contact-links {{
 &bull;  &bull;  &bull;  &bull; font-size: 13px;
 &bull;  &bull;  &bull;  &bull; color: #374151;
 &bull;  &bull;  &bull;  &bull; line-height: 1.5;
 &bull;  &bull;  &bull;  &bull; margin-bottom: 2px;
 &bull;  &bull; }}
 &bull;  &bull; .resume-contact-links a {{
 &bull;  &bull;  &bull;  &bull; color: #1d4ed8;
 &bull;  &bull;  &bull;  &bull; text-decoration: underline;
 &bull;  &bull; }}
 &bull;  &bull; .resume-immediate-joiner {{
 &bull;  &bull;  &bull;  &bull; font-size: 13.5px;
 &bull;  &bull;  &bull;  &bull; font-weight: 700;
 &bull;  &bull;  &bull;  &bull; color: #111827;
 &bull;  &bull;  &bull;  &bull; margin-top: 3px;
 &bull;  &bull; }}
 &bull;  &bull; section {{
 &bull;  &bull;  &bull;  &bull; margin-bottom: 18px;
 &bull;  &bull; }}
 &bull;  &bull; h2 {{
 &bull;  &bull;  &bull;  &bull; font-size: 15px;
 &bull;  &bull;  &bull;  &bull; text-transform: uppercase;
 &bull;  &bull;  &bull;  &bull; color: #1e3a8a;
 &bull;  &bull;  &bull;  &bull; border-bottom: 1px solid #cbd5e1;
 &bull;  &bull;  &bull;  &bull; padding-bottom: 4px;
 &bull;  &bull;  &bull;  &bull; margin: 16px 0 10px 0;
 &bull;  &bull;  &bull;  &bull; letter-spacing: 0.5px;
 &bull;  &bull; }}
 &bull;  &bull; .summary-text {{
 &bull;  &bull;  &bull;  &bull; font-size: 13.5px;
 &bull;  &bull;  &bull;  &bull; color: #334155;
 &bull;  &bull;  &bull;  &bull; text-align: justify;
 &bull;  &bull; }}
 &bull;  &bull; ul.skills-list {{
 &bull;  &bull;  &bull;  &bull; list-style: none;
 &bull;  &bull;  &bull;  &bull; padding: 0;
 &bull;  &bull;  &bull;  &bull; margin: 0;
 &bull;  &bull;  &bull;  &bull; font-size: 13px;
 &bull;  &bull; }}
 &bull;  &bull; ul.skills-list li {{
 &bull;  &bull;  &bull;  &bull; margin-bottom: 4px;
 &bull;  &bull; }}
 &bull;  &bull; .job-header {{
 &bull;  &bull;  &bull;  &bull; display: flex;
 &bull;  &bull;  &bull;  &bull; justify-content: space-between;
 &bull;  &bull;  &bull;  &bull; font-size: 14px;
 &bull;  &bull;  &bull;  &bull; font-weight: bold;
 &bull;  &bull;  &bull;  &bull; color: #0f172a;
 &bull;  &bull; }}
 &bull;  &bull; .job-sub {{
 &bull;  &bull;  &bull;  &bull; font-size: 13px;
 &bull;  &bull;  &bull;  &bull; color: #64748b;
 &bull;  &bull;  &bull;  &bull; font-style: italic;
 &bull;  &bull;  &bull;  &bull; margin-bottom: 8px;
 &bull;  &bull; }}
 &bull;  &bull; ul.experience-list {{
 &bull;  &bull;  &bull;  &bull; padding-left: 20px;
 &bull;  &bull;  &bull;  &bull; margin: 0;
 &bull;  &bull; }}
 &bull;  &bull; .bullet-item {{
 &bull;  &bull;  &bull;  &bull; margin-bottom: 10px;
 &bull;  &bull;  &bull;  &bull; font-size: 13px;
 &bull;  &bull;  &bull;  &bull; color: #1e293b;
 &bull;  &bull; }}
 &bull;  &bull; .kw-container {{
 &bull;  &bull;  &bull;  &bull; margin-top: 3px;
 &bull;  &bull; }}
 &bull;  &bull; .kw-tag {{
 &bull;  &bull;  &bull;  &bull; display: inline-block;
 &bull;  &bull;  &bull;  &bull; background: #eff6ff;
 &bull;  &bull;  &bull;  &bull; color: #1d4ed8;
 &bull;  &bull;  &bull;  &bull; border: 1px solid #bfdbfe;
 &bull;  &bull;  &bull;  &bull; font-size: 11px;
 &bull;  &bull;  &bull;  &bull; padding: 1px 6px;
 &bull;  &bull;  &bull;  &bull; border-radius: 4px;
 &bull;  &bull;  &bull;  &bull; font-weight: 500;
 &bull;  &bull;  &bull;  &bull; margin-right: 4px;
 &bull;  &bull; }}
 &bull;  &bull; @media print {{
 &bull;  &bull;  &bull;  &bull; body {{
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; padding: 0;
 &bull;  &bull;  &bull;  &bull; }}
 &bull;  &bull;  &bull;  &bull; .kw-container {{
 &bull;  &bull;  &bull;  &bull;  &bull;  &bull; display: none !important;
 &bull;  &bull;  &bull;  &bull; }}
 &bull;  &bull; }}
</style>
</head>
<body>
<div class="resume-container">
 &bull;  &bull; <header>
 &bull;  &bull;  &bull;  &bull; <div class="resume-name">P R A C H I &bull;  J A I N</div>
 &bull;  &bull;  &bull;  &bull; <div class="resume-contact-line">Hyderabad, India | +91-6266761271 | prachijain6699@gmail.com</div>
 &bull;  &bull;  &bull;  &bull; <div class="resume-contact-links">LinkedIn: <a href="https://linkedin.com/in/prachi-jain6584" target="_blank" rel="noopener noreferrer">linkedin.com/in/prachi-jain6584</a> &bull; GitHub: <a href="https://github.com/PrachiJain123" target="_blank" rel="noopener noreferrer">github.com/PrachiJain123</a> &bull; Portfolio: <a href="https://prachijain123.github.io/" target="_blank" rel="noopener noreferrer">https://prachijain123.github.io/</a></div>
 &bull;  &bull;  &bull;  &bull; <div class="resume-immediate-joiner">Immediate Joiner</div>
 &bull;  &bull; </header>

 &bull;  &bull; {sections_html}
</div>
</body>
</html>
"""
 &bull;  &bull; return html


def format_xyz_bullet_table_markdown(report: ATSOptimizationReport) -> str:
 &bull;  &bull; """Creates a Markdown comparison table showing original vs XYZ rewritten bullets."""
 &bull;  &bull; lines = [
 &bull;  &bull;  &bull;  &bull; "| # | Original Bullet | Google XYZ Rewritten Bullet | Infused Keywords |",
 &bull;  &bull;  &bull;  &bull; "|---|---|---|---|",
 &bull;  &bull; ]
 &bull;  &bull; for i, b in enumerate(report.optimized_bullets, 1):
 &bull;  &bull;  &bull;  &bull; orig_clean = b.original.replace("|", "\\|").replace("\n", " ")
 &bull;  &bull;  &bull;  &bull; rewr_clean = b.rewritten.replace("|", "\\|").replace("\n", " ")
 &bull;  &bull;  &bull;  &bull; kws = ", ".join(b.keywords_infused) if b.keywords_infused else "—"
 &bull;  &bull;  &bull;  &bull; lines.append(f"| {i} | {orig_clean} | **{rewr_clean}** | `{kws}` |")
 &bull;  &bull; return "\n".join(lines)


def format_analysis_summary_markdown(report: ATSOptimizationReport) -> str:
 &bull;  &bull; """Generates an executive analysis markdown report detailing ATS keyword scores and XYZ impact."""
 &bull;  &bull; status_badge = "✅ PASSED (>= 90%)" if report.passed_90 else "⚠️ IN PROGRESS"
 &bull;  &bull; 
 &bull;  &bull; md = [
 &bull;  &bull;  &bull;  &bull; f"## 🎯 ATS Keyword Match & Google XYZ Optimization Audit",
 &bull;  &bull;  &bull;  &bull; f"",
 &bull;  &bull;  &bull;  &bull; f"- **Initial Match Score:** `{report.initial_score:.1f}%`",
 &bull;  &bull;  &bull;  &bull; f"- **Post-XYZ Rewriting Score:** `{report.post_rewrite_score:.1f}%`",
 &bull;  &bull;  &bull;  &bull; f"- **Final Optimized Score:** **`{report.final_score:.1f}%`**",
 &bull;  &bull;  &bull;  &bull; f"- **90%+ ATS Target Threshold:** **{status_badge}**",
 &bull;  &bull;  &bull;  &bull; f"- **Optimization Iterations:** `{report.iterations_run}`",
 &bull;  &bull;  &bull;  &bull; f"- **Page Budget:** `{report.original_page_count} page(s)` (estimated output: `{report.estimated_output_pages}`)",
 &bull;  &bull;  &bull;  &bull; f"- **Max Bullet Words:** `{report.max_bullet_words}`",
 &bull;  &bull;  &bull;  &bull; f"",
 &bull;  &bull;  &bull;  &bull; f"### 📊 Keyword Coverage Metrics",
 &bull;  &bull;  &bull;  &bull; f"- **Initial Matched Keywords ({len(report.initial_matched_keywords)}):** {', '.join(f'`{k}`' for k in report.initial_matched_keywords) or 'None'}",
 &bull;  &bull;  &bull;  &bull; f"- **Initial Missing Keywords ({len(report.initial_missing_keywords)}):** {', '.join(f'`{k}`' for k in report.initial_missing_keywords) or 'None'}",
 &bull;  &bull;  &bull;  &bull; f"- **Final Keyword Coverage ({len(report.post_rewrite_matched)}):** {', '.join(f'`{k}`' for k in report.post_rewrite_matched)}",
 &bull;  &bull;  &bull;  &bull; f"",
 &bull;  &bull;  &bull;  &bull; f"### ⚙️ Optimization Audit Trail",
 &bull;  &bull; ]
 &bull;  &bull; for note in report.optimization_notes:
 &bull;  &bull;  &bull;  &bull; md.append(f"- {note}")

 &bull;  &bull; return "\n".join(md)
