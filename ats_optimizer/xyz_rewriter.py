"""Google XYZ Formula Experience Bullet Rewriting Engine.

Formula:
  "Accomplished [X] as measured by [Y], by doing [Z]"
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class XYZBullet:
    """Represents a single resume experience bullet point rewritten into the XYZ formula."""
    original: str
    rewritten: str
    accomplished_x: str
    measured_by_y: str
    doing_z: str
    keywords_infused: list[str] = field(default_factory=list)
    role_or_project: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "original": self.original,
            "rewritten": self.rewritten,
            "accomplished_x": self.accomplished_x,
            "measured_by_y": self.measured_by_y,
            "doing_z": self.doing_z,
            "keywords_infused": self.keywords_infused,
            "role_or_project": self.role_or_project,
        }


def extract_xyz_components(bullet: str) -> tuple[str, str, str]:
    """Attempts to parse [X], [Y], and [Z] components from a bullet string."""
    clean = bullet.strip().lstrip("-*• ")
    
    # Pattern 1: Accomplished X [as measured] by Y [by doing / through] Z
    m1 = re.search(r"^(.*?)(?:,\s*|\s+)as measured by (.*?)(?:,\s*|\s+)by (.*)$", clean, re.IGNORECASE)
    if m1:
        return m1.group(1).strip(), m1.group(2).strip(), m1.group(3).strip()

    # Pattern 2: Verb X by Y% by doing Z
    m2 = re.search(r"^(.*?)(?:by\s+(\d+%|\$[\d,]+[kKmM]?|[\d\.]+x|[\d,]+\+? [a-zA-Z]+))(?:,\s*|\s+)(?:by|through|utilizing|via)\s+(.*)$", clean, re.IGNORECASE)
    if m2:
        return m2.group(1).strip(), m2.group(2).strip(), m2.group(3).strip()

    # Fallback decomposition
    words = clean.split()
    if len(words) > 12:
        half = len(words) // 2
        return " ".join(words[:5]), "quantified performance gains of 30%+", " ".join(words[5:])
    return clean, "verified operational benchmarks", "implementing best-practice technical workflows"


def _trim_to_word_limit(text: str, max_words: int) -> str:
    """Trim text to max_words while trying to end at a sentence/clause boundary."""
    words = text.split()
    if len(words) <= max_words:
        return text
    trimmed = " ".join(words[:max_words])
    # Try to end at a period or comma
    last_period = trimmed.rfind(".")
    last_comma = trimmed.rfind(",")
    cut_point = max(last_period, last_comma)
    if cut_point > len(trimmed) // 2:
        trimmed = trimmed[:cut_point + 1].strip()
    if not trimmed.endswith("."):
        trimmed = trimmed.rstrip(",;:") + "."
    return trimmed


def generate_rule_based_xyz(
    original_bullet: str,
    target_keywords: list[str] | None = None,
    max_words: int = 45
) -> XYZBullet:
    """Transforms a raw resume bullet into the Google XYZ formula using domain heuristics.
    
    Accomplished [X] as measured by [Y], by doing [Z]
    
    Args:
        original_bullet: The raw bullet text.
        target_keywords: Pool of missing keywords to infuse.
        max_words: Maximum word count for the rewritten bullet (for page budgeting).
    """
    clean = original_bullet.strip().lstrip("-*• ")
    lowered = clean.lower()
    
    infused: list[str] = []
    avail_keywords = list(target_keywords or [])

    # Identify action and theme
    if any(k in lowered for k in ["dashboard", "looker", "tableau", "bi", "visualiz"]):
        kw = _pick_and_remove(avail_keywords, ["Looker", "Tableau", "SQL", "Data Modeling", "ETL"])
        infused.extend(kw)
        tech_clause = " and ".join(kw) if kw else "SQL queries and interactive dashboard automation"
        x = "Accelerated executive decision-making turnaround"
        y = "38% reduction in recurring reporting latency (saving 15+ engineering hours weekly)"
        z = f"architecting automated {tech_clause} data pipelines with real-time KPI filters"
        rewritten = f"Accelerated executive decision-making turnaround, as measured by a 38% reduction in recurring reporting latency (saving 15+ engineering hours weekly), by architecting automated {tech_clause} data pipelines with real-time KPI filters."

    elif any(k in lowered for k in ["sql", "query", "database", "mysql", "postgres", "pipeline"]):
        kw = _pick_and_remove(avail_keywords, ["SQL", "PostgreSQL", "MySQL", "Snowflake", "ETL", "Data Warehousing"])
        infused.extend(kw)
        tech_clause = ", ".join(kw) if kw else "SQL query indexing, partitioning, and automated ETL pipelines"
        x = "Optimized core database throughput and batch query efficiency"
        y = "45% reduction in execution runtime across 2.5M+ records"
        z = f"refactoring legacy data ingestion scripts and deploying modular {tech_clause} schemas"
        rewritten = f"Optimized core database throughput and batch query efficiency, as measured by a 45% reduction in execution runtime across 2.5M+ records, by refactoring legacy data ingestion scripts and deploying modular {tech_clause} schemas."

    elif any(k in lowered for k in ["api", "backend", "fastapi", "python", "service", "microservice"]):
        kw = _pick_and_remove(avail_keywords, ["Python", "FastAPI", "RESTful APIs", "Microservices", "Docker", "Redis"])
        infused.extend(kw)
        tech_clause = ", ".join(kw) if kw else "Python REST APIs, asynchronous handlers, and Redis caching"
        x = "Scaled high-concurrency backend services"
        y = "handling 5,000+ requests/sec with a 99.95% uptime SLA"
        z = f"developing decoupled {tech_clause} with automated CI/CD deployment pipelines"
        rewritten = f"Scaled high-concurrency backend services, as measured by handling 5,000+ requests/sec with a 99.95% uptime SLA, by developing decoupled {tech_clause} with automated CI/CD deployment pipelines."

    elif any(k in lowered for k in ["model", "ml", "ai", "machine learning", "predict", "analy"]):
        kw = _pick_and_remove(avail_keywords, ["Python", "Scikit-Learn", "PyTorch", "Pandas", "Feature Engineering"])
        infused.extend(kw)
        tech_clause = ", ".join(kw) if kw else "Python, Pandas, and Scikit-Learn feature engineering pipelines"
        x = "Boosted predictive accuracy of business forecasting models"
        y = "an 18.5% increase in F1-score and $110K annualized cost avoidance"
        z = f"engineering robust feature stores and cross-validated predictive models using {tech_clause}"
        rewritten = f"Boosted predictive accuracy of business forecasting models, as measured by an 18.5% increase in F1-score and $110K annualized cost avoidance, by engineering robust feature stores and cross-validated predictive models using {tech_clause}."

    else:
        # General technical bullet rewrite
        kw = _pick_and_remove(avail_keywords, ["Python", "SQL", "Git", "Agile", "CI/CD"])
        infused.extend(kw)
        tech_clause = f" utilizing {', '.join(kw)}" if kw else " using automated testing and agile sprint cycles"
        x = f"Streamlined technical delivery and operational workflow reliability"
        y = "a 32% increase in deployment velocity and zero production regressions"
        z = f"modernizing codebase architecture{tech_clause} and standardizing documentation"
        rewritten = f"Streamlined technical delivery and operational workflow reliability, as measured by a 32% increase in deployment velocity and zero production regressions, by modernizing codebase architecture{tech_clause} and standardizing documentation."

    # Apply page-budget word limit
    if max_words and max_words > 0:
        rewritten = _trim_to_word_limit(rewritten, max_words)

    return XYZBullet(
        original=clean,
        rewritten=rewritten,
        accomplished_x=x,
        measured_by_y=y,
        doing_z=z,
        keywords_infused=infused,
    )


def _pick_and_remove(source: list[str], preferred: list[str]) -> list[str]:
    """Select matching preferred keywords from the available pool and remove them to avoid repetition."""
    selected = []
    source_lower = [s.lower() for s in source]
    for pref in preferred:
        if pref.lower() in source_lower:
            idx = source_lower.index(pref.lower())
            actual = source.pop(idx)
            source_lower.pop(idx)
            selected.append(actual)
            if len(selected) >= 2:
                break
    return selected
