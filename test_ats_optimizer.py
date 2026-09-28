"""Unit and integration tests for ATS Resume Optimizer.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

# Ensure utf-8 stdout
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from ats_optimizer.ats_matcher import run_ats_optimization_loop
from ats_optimizer.client import AntigravityOptimizerClient
from ats_optimizer.config import DEFAULT_MODEL, TARGET_ATS_SCORE
from ats_optimizer.formatter import (
    format_html_resume,
    format_markdown_resume,
    format_xyz_bullet_table_markdown,
)
from ats_optimizer.keyword_engine import (
    calculate_ats_match,
    canonical_name,
    extract_keywords_heuristics,
)
from ats_optimizer.parser import clean_text, extract_bullet_points, extract_text_from_pdf
from ats_optimizer.samples import SAMPLE_JOB_DESCRIPTIONS, SAMPLE_RESUME_TEXT
from ats_optimizer.xyz_rewriter import generate_rule_based_xyz


class TestATSOptimizer(unittest.TestCase):

    def test_clean_text_and_bullet_extraction(self):
        sample = """
        • Developed high throughput REST APIs in Python and FastAPI.
        • Optimized SQL database queries reducing latency.
        - Spearheaded migration to AWS and Docker.
        """
        cleaned = clean_text(sample)
        bullets = extract_bullet_points(cleaned)
        self.assertGreaterEqual(len(bullets), 2)
        self.assertTrue(any("FastAPI" in b or "Python" in b for b in bullets))

    def test_pdf_extraction_if_file_exists(self):
        pdf_path = Path("Prachi_Jain_Resume.pdf")
        if pdf_path.is_file():
            text = extract_text_from_pdf(pdf_path)
            self.assertGreater(len(text), 500)
            self.assertIn("PRACHI", text.upper())

    def test_keyword_extraction_heuristics(self):
        jd_sample = "Must have strong skills in Python, SQL, Docker, AWS, Snowflake, Airflow, and CI/CD."
        kws, cats, freqs = extract_keywords_heuristics(jd_sample)
        self.assertIn("Python", kws)
        self.assertIn("SQL", kws)
        self.assertIn("Docker", kws)
        self.assertIn("AWS", kws)
        self.assertIn("Snowflake", kws)
        self.assertIn("Airflow", kws)
        self.assertIn("CI/CD", kws)

    def test_ats_match_calculation(self):
        jd_kws = ["Python", "SQL", "Docker", "AWS", "Snowflake"]
        res_kws = ["Python", "SQL"]
        match = calculate_ats_match(jd_kws, res_kws)
        self.assertAlmostEqual(match.ats_score, 40.0, delta=1.0)
        self.assertFalse(match.passed_90_threshold)
        self.assertEqual(match.matched_keywords, ["Python", "SQL"])
        self.assertIn("Docker", match.missing_keywords)
        self.assertIn("Snowflake", match.missing_keywords)

    def test_xyz_formula_generation(self):
        original = "Responsible for building data pipelines and Looker dashboards for reporting."
        xyz = generate_rule_based_xyz(original, target_keywords=["Snowflake", "ETL"])
        self.assertIn("as measured by", xyz.rewritten)
        self.assertIn("by", xyz.rewritten)
        self.assertTrue(len(xyz.accomplished_x) > 0)
        self.assertTrue(len(xyz.measured_by_y) > 0)
        self.assertTrue(len(xyz.doing_z) > 0)

    def test_90_plus_ats_optimization_loop(self):
        jd_kws = ["Python", "SQL", "Docker", "AWS", "Snowflake", "Airflow", "FastAPI", "PostgreSQL", "Kafka", "CI/CD"]
        res_kws = ["Python", "SQL"]
        initial_bullets = [
            "Built data pipelines in Python.",
            "Wrote SQL queries for reports."
        ]
        rewritten = [generate_rule_based_xyz(b, ["Docker", "AWS"]) for b in initial_bullets]

        report = run_ats_optimization_loop(
            jd_keywords=jd_kws,
            resume_keywords=res_kws,
            initial_bullets=initial_bullets,
            rewritten_bullets=rewritten,
            target_score=90.0,
        )

        self.assertGreaterEqual(report.final_score, 90.0)
        self.assertTrue(report.passed_90)
        self.assertGreater(report.final_score, report.initial_score)

    def test_formatting_markdown_and_html(self):
        jd_kws = ["Python", "SQL", "AWS", "Docker", "CI/CD"]
        res_kws = ["Python", "SQL"]
        bullets = [generate_rule_based_xyz("Developed Python backend.", ["AWS", "Docker"])]
        report = run_ats_optimization_loop(
            jd_keywords=jd_kws,
            resume_keywords=res_kws,
            initial_bullets=["Developed Python backend."],
            rewritten_bullets=bullets,
            target_score=90.0,
        )

        md = format_markdown_resume(report, SAMPLE_RESUME_TEXT)
        html = format_html_resume(report, SAMPLE_RESUME_TEXT)
        table = format_xyz_bullet_table_markdown(report)

        self.assertIn("# PRACHI JAIN", md.upper())
        self.assertIn("CORE TECHNICAL SKILLS", md)
        self.assertIn("as measured by", md)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("| Google XYZ Rewritten Bullet |", table)

    def test_client_configuration(self):
        client = AntigravityOptimizerClient(model=DEFAULT_MODEL)
        self.assertEqual(client.model, "gemini-3.1-pro")
        self.assertEqual(DEFAULT_MODEL, "gemini-3.1-pro")
        self.assertEqual(TARGET_ATS_SCORE, 90.0)


if __name__ == "__main__":
    unittest.main()
