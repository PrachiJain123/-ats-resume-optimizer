"""Command-Line Interface for ATS Resume Optimizer powered by Antigravity SDK & Gemini 3.1 Pro.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

# Fix Windows console cp1252 encoding for unicode characters
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from ats_optimizer.client import AntigravityOptimizerClient
from ats_optimizer.config import DEFAULT_MODEL, TARGET_ATS_SCORE, get_gemini_api_key
from ats_optimizer.formatter import (
    format_analysis_summary_markdown,
    format_html_resume,
    format_markdown_resume,
    format_xyz_bullet_table_markdown,
)
from ats_optimizer.parser import clean_text, extract_text_from_pdf
from ats_optimizer.samples import SAMPLE_JOB_DESCRIPTIONS, get_default_resume_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ATS Resume Optimizer using Google Antigravity SDK and Gemini 3.1 Pro."
    )
    parser.add_argument("--jd", type=str, help="Path to Job Description file (.txt, .md)")
    parser.add_argument("--resume", type=str, help="Path to Resume file (.pdf, .txt, .md)")
    parser.add_argument("--api-key", type=str, default=None, help="Gemini API Key override")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="Model target (default: gemini-3.1-pro)")
    parser.add_argument("--target-score", type=float, default=TARGET_ATS_SCORE, help="Target ATS score (default: 90.0)")
    parser.add_argument("--output-dir", type=str, default="./output", help="Directory for output files")
    parser.add_argument("--sample", action="store_true", help="Run with built-in sample JD and workspace resume")
    return parser.parse_args()


async def run_cli() -> None:
    args = parse_args()
    print("=" * 70)
    print("🚀 Google Antigravity SDK — ATS Resume Optimizer (Gemini 3.1 Pro)")
    print("=" * 70)

    # 1. Determine Inputs
    if args.sample or (not args.jd and not args.resume):
        print("📌 Loading sample Job Description and Resume...")
        jd_title = list(SAMPLE_JOB_DESCRIPTIONS.keys())[0]
        jd_text = SAMPLE_JOB_DESCRIPTIONS[jd_title]
        resume_text = get_default_resume_text()
        print(f"   Selected JD: {jd_title}")
        print(f"   Resume Length: {len(resume_text)} characters")
    else:
        if not args.jd or not os.path.exists(args.jd):
            print(f"❌ Error: Job Description file not found: {args.jd}")
            sys.exit(1)
        with open(args.jd, "r", encoding="utf-8") as f:
            jd_text = f.read()

        if not args.resume or not os.path.exists(args.resume):
            print(f"❌ Error: Resume file not found: {args.resume}")
            sys.exit(1)

        if args.resume.lower().endswith(".pdf"):
            resume_text = extract_text_from_pdf(args.resume)
        else:
            with open(args.resume, "r", encoding="utf-8") as f:
                resume_text = clean_text(f.read())

    # 2. Check API Key
    api_key = get_gemini_api_key(args.api_key)
    if api_key:
        print(f"🔑 Gemini API Key: Detected (Active with model '{args.model}')")
    else:
        print("⚠️ Notice: No GEMINI_API_KEY detected in environment or .env.")
        print("   Running in High-Fidelity Heuristic Optimization mode.")
        print("   Set GEMINI_API_KEY to activate live Gemini 3.1 Pro generation.")

    # 3. Initialize Optimizer Client
    client = AntigravityOptimizerClient(api_key=api_key, model=args.model)

    print("\n⏳ Step 1: Extracting technical keywords from JD & Resume...")
    jd_kws, res_kws, meta = await client.extract_keywords(jd_text, resume_text)
    print(f"   ✓ JD Keywords ({len(jd_kws)}): {', '.join(jd_kws[:8])}...")
    print(f"   ✓ Resume Keywords ({len(res_kws)}): {', '.join(res_kws[:8])}...")

    print("\n⏳ Step 2: Rewriting experience bullets using Google's XYZ formula...")
    print("   Formula: Accomplished [X] as measured by [Y], by doing [Z]")
    report = await client.optimize_resume(jd_text, resume_text, target_score=args.target_score)

    print(f"\n⏳ Step 3: Checking ATS keyword match & 90+ threshold...")
    print(f"   • Initial Match Score: {report.initial_score:.1f}%")
    print(f"   • Post-XYZ Rewriting Score: {report.post_rewrite_score:.1f}%")
    print(f"   • Final Optimized Score: {report.final_score:.1f}%")

    if report.passed_90:
        print("   🎯 SUCCESS: Achieved >= 90.0% ATS Keyword Match!")
    else:
        print(f"   ⚠️ Reached {report.final_score:.1f}% match.")

    # Print Bullet Sample
    print("\n" + "=" * 70)
    print("📝 SAMPLE REWRITTEN GOOGLE XYZ BULLETS")
    print("=" * 70)
    for i, b in enumerate(report.optimized_bullets[:3], 1):
        print(f"\n[{i}] Original:")
        print(f"    \"{b.original}\"")
        print(f"    Google XYZ Rewritten:")
        print(f"    \"{b.rewritten}\"")
        if b.keywords_infused:
            print(f"    Keywords Infused: {', '.join(b.keywords_infused)}")

    # 4. Generate Formatted Outputs
    print("\n⏳ Step 4: Generating Formatted Outputs (Markdown, HTML, JSON)...")
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    md_resume = format_markdown_resume(report, resume_text)
    html_resume = format_html_resume(report, resume_text)
    md_audit = format_analysis_summary_markdown(report)
    md_table = format_xyz_bullet_table_markdown(report)

    # Save Markdown Resume
    md_file = out_dir / "resume_optimized.md"
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(md_resume)

    # Save HTML Resume
    html_file = out_dir / "resume_optimized.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_resume)

    # Save Audit Report
    audit_file = out_dir / "ats_audit_report.md"
    with open(audit_file, "w", encoding="utf-8") as f:
        f.write(md_audit + "\n\n### 🔄 Experience Bullets Comparison\n\n" + md_table)

    # Save JSON Report
    json_file = out_dir / "ats_report.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(report.to_dict(), f, indent=2)

    print(f"   ✓ Formatted Markdown Resume : {md_file.resolve()}")
    print(f"   ✓ Formatted HTML Resume     : {html_file.resolve()}")
    print(f"   ✓ ATS Audit Report (MD)     : {audit_file.resolve()}")
    print(f"   ✓ ATS Structured Data (JSON): {json_file.resolve()}")

    print("\n✨ Optimization complete! You can open the HTML resume in your browser to print to PDF.")
    print("=" * 70)


def main() -> None:
    asyncio.run(run_cli())


if __name__ == "__main__":
    main()
