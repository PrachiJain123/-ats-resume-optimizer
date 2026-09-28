"""Antigravity SDK Client using gemini-3.1-pro for ATS Optimization and Bullet Rewriting.
"""

from __future__ import annotations

import asyncio
import json
import logging
import re
from typing import Any

from .config import DEFAULT_MODEL, get_gemini_api_key
from .keyword_engine import (
    calculate_ats_match,
    canonical_name,
    extract_keywords_heuristics,
)
from .xyz_rewriter import XYZBullet, generate_rule_based_xyz
from .ats_matcher import ATSOptimizationReport, run_ats_optimization_loop

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an elite Google Talent Acquisition & ATS Systems Architect specializing in resume optimization.
Your mission is to analyze Job Descriptions and Resumes, extract technical competencies, rewrite experience bullet points strictly adhering to Google's official XYZ Formula ("Accomplished [X] as measured by [Y], by doing [Z]"), and guarantee a 90%+ ATS keyword match without keyword stuffing.
"""


class AntigravityOptimizerClient:
    """Orchestrates resume optimization using Google Antigravity SDK and gemini-3.1-pro."""

    def __init__(self, api_key: str | None = None, model: str = DEFAULT_MODEL):
        self.api_key = get_gemini_api_key(api_key)
        self.model = model
        self.has_api_key = bool(self.api_key and not self.api_key.startswith("dummy"))

    async def _call_agent(self, prompt: str) -> str:
        """Invokes google.antigravity.Agent with gemini-3.1-pro."""
        from google.antigravity import Agent, LocalAgentConfig, CapabilitiesConfig

        config = LocalAgentConfig(
            model=self.model,
            api_key=self.api_key,
            system_instructions=SYSTEM_PROMPT,
            capabilities=CapabilitiesConfig(),
        )

        async with Agent(config) as agent:
            response = await agent.chat(prompt)
            output_text = await response.text()
            return output_text

    async def extract_keywords(
        self,
        jd_text: str,
        resume_text: str
    ) -> tuple[list[str], list[str], dict[str, Any]]:
        """Extracts technical keywords from JD and Resume using Gemini 3.1 Pro or fallback engine."""
        if not self.has_api_key:
            return self._extract_keywords_fallback(jd_text, resume_text)

        prompt = f"""Extract all technical keywords from both the Job Description and the Resume.
Categorize each into one of:
- Languages
- Frameworks & Libraries
- Cloud & DevOps
- Databases & Big Data
- Architecture & Methodologies
- Analytics & Tools

Also classify JD keywords by priority ("Critical" if required or mentioned multiple times, else "Standard").

Format your response strictly as valid JSON with this structure:
{{
  "jd_keywords": [
    {{"name": "Python", "category": "Languages", "priority": "Critical"}},
    ...
  ],
  "resume_keywords": [
    {{"name": "SQL", "category": "Languages"}},
    ...
  ]
}}

Job Description:
\"\"\"{jd_text[:4000]}\"\"\"

Resume:
\"\"\"{resume_text[:4000]}\"\"\"
"""
        try:
            raw_response = await self._call_agent(prompt)
            data = _parse_json_from_response(raw_response)
            jd_list = [canonical_name(item["name"]) for item in data.get("jd_keywords", [])]
            res_list = [canonical_name(item["name"]) for item in data.get("resume_keywords", [])]
            meta = {
                "source": "gemini-3.1-pro",
                "jd_details": data.get("jd_keywords", []),
                "resume_details": data.get("resume_keywords", [])
            }
            if not jd_list:
                return self._extract_keywords_fallback(jd_text, resume_text)
            return jd_list, res_list, meta
        except Exception as e:
            logger.warning(f"Gemini 3.1 Pro keyword extraction error ({e}); using heuristic engine.")
            return self._extract_keywords_fallback(jd_text, resume_text)

    def _extract_keywords_fallback(
        self,
        jd_text: str,
        resume_text: str
    ) -> tuple[list[str], list[str], dict[str, Any]]:
        jd_kws, jd_cats, jd_freqs = extract_keywords_heuristics(jd_text)
        res_kws, res_cats, res_freqs = extract_keywords_heuristics(resume_text)
        meta = {
            "source": "heuristic_engine",
            "jd_categories": jd_cats,
            "resume_categories": res_cats,
            "jd_frequencies": jd_freqs
        }
        return jd_kws, res_kws, meta

    async def rewrite_bullets_xyz(
        self,
        bullets: list[str],
        missing_keywords: list[str],
        jd_context: str = ""
    ) -> list[XYZBullet]:
        """Rewrites experience bullets using the Google XYZ formula."""
        if not bullets:
            return []

        if not self.has_api_key:
            return self._rewrite_bullets_fallback(bullets, missing_keywords)

        prompt = f"""Rewrite each of the following resume experience bullets strictly using the Google XYZ Formula:
"Accomplished [X] as measured by [Y], by doing [Z]"

Rules:
1. [X] = Active verb + quantifiable impact/accomplishment
2. [Y] = Measurable benchmark, metric, latency reduction, cost savings, or percentage
3. [Z] = Specific technical action taken, architecture chosen, and tools applied
4. Seamlessly incorporate these target missing keywords where logically fitting: {', '.join(missing_keywords[:15])}
5. Return strictly valid JSON containing a list of objects with fields:
   - "original": original bullet
   - "rewritten": the complete XYZ bullet
   - "accomplished_x": [X] component
   - "measured_by_y": [Y] component
   - "doing_z": [Z] component
   - "keywords_infused": list of keywords incorporated

Original Bullets:
{json.dumps(bullets[:10], indent=2)}
"""
        try:
            raw_response = await self._call_agent(prompt)
            data = _parse_json_from_response(raw_response)
            results: list[XYZBullet] = []
            
            raw_items = data if isinstance(data, list) else data.get("bullets", [])
            for item in raw_items:
                results.append(
                    XYZBullet(
                        original=item.get("original", ""),
                        rewritten=item.get("rewritten", ""),
                        accomplished_x=item.get("accomplished_x", ""),
                        measured_by_y=item.get("measured_by_y", ""),
                        doing_z=item.get("doing_z", ""),
                        keywords_infused=item.get("keywords_infused", []),
                    )
                )
            if not results:
                return self._rewrite_bullets_fallback(bullets, missing_keywords)
            return results
        except Exception as e:
            logger.warning(f"Gemini 3.1 Pro XYZ rewrite error ({e}); using heuristic engine.")
            return self._rewrite_bullets_fallback(bullets, missing_keywords)

    def _rewrite_bullets_fallback(
        self,
        bullets: list[str],
        missing_keywords: list[str]
    ) -> list[XYZBullet]:
        pool = list(missing_keywords)
        results = []
        for b in bullets:
            results.append(generate_rule_based_xyz(b, pool))
        return results

    async def optimize_resume(
        self,
        jd_text: str,
        resume_text: str,
        target_score: float = 90.0
    ) -> ATSOptimizationReport:
        """Full pipeline: Keyword Extraction -> XYZ Bullet Rewriting -> 90+ ATS Check & Optimization Loop."""
        # 1. Extract raw bullets
        from .parser import extract_bullet_points
        raw_bullets = extract_bullet_points(resume_text)
        if not raw_bullets:
            raw_bullets = [
                "Developed data analytics pipelines and automated weekly executive dashboards.",
                "Optimized SQL queries and resolved reporting latency issues across customer databases.",
                "Collaborated with cross-functional product teams to deliver feature analytics."
            ]

        # 2. Extract technical keywords
        jd_kws, res_kws, meta = await self.extract_keywords(jd_text, resume_text)

        # Baseline match
        initial_match = calculate_ats_match(jd_kws, res_kws)

        # 3. Rewrite experience bullets with missing keywords
        rewritten_bullets = await self.rewrite_bullets_xyz(
            raw_bullets,
            initial_match.missing_keywords,
            jd_context=jd_text
        )

        # 4. Check & optimize for 90+ ATS score
        report = run_ats_optimization_loop(
            jd_keywords=jd_kws,
            resume_keywords=res_kws,
            initial_bullets=raw_bullets,
            rewritten_bullets=rewritten_bullets,
            target_score=target_score,
        )

        return report

    def optimize_resume_sync(
        self,
        jd_text: str,
        resume_text: str,
        target_score: float = 90.0
    ) -> ATSOptimizationReport:
        """Synchronous wrapper for optimize_resume."""
        return asyncio.run(self.optimize_resume(jd_text, resume_text, target_score))


def _parse_json_from_response(text: str) -> Any:
    """Safely extracts JSON from an LLM response containing markdown codeblocks or prose."""
    # Look for ```json ... ``` blocks
    code_block = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if code_block:
        clean_text = code_block.group(1).strip()
    else:
        clean_text = text.strip()

    # Find boundaries of JSON array or object
    json_start = -1
    for i, ch in enumerate(clean_text):
        if ch in ("{", "["):
            json_start = i
            break
            
    if json_start != -1:
        clean_text = clean_text[json_start:]
        # Reverse find matching end
        last_obj = clean_text.rfind("}")
        last_arr = clean_text.rfind("]")
        end_idx = max(last_obj, last_arr)
        if end_idx != -1:
            clean_text = clean_text[:end_idx + 1]

    return json.loads(clean_text)
