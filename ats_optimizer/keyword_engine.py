"""Technical keyword extraction, taxonomy categorization, and ATS scoring engine.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Any

# Standard comprehensive tech keyword dictionary for deterministic extraction & fallback
TECH_TAXONOMY: dict[str, list[str]] = {
    "Languages": [
        "python", "sql", "java", "c++", "c#", "c", "golang", "go", "typescript",
        "javascript", "r", "scala", "rust", "ruby", "php", "bash", "shell", "powershell", "dart", "kotlin"
    ],
    "Frameworks & Libraries": [
        "pandas", "numpy", "scipy", "scikit-learn", "sklearn", "tensorflow", "pytorch",
        "keras", "fastapi", "flask", "django", "react", "react.js", "angular", "vue.js",
        "next.js", "node.js", "express", "spring boot", "langchain", "llamaindex", "hugging face",
        "transformers", "opencv", "matplotlib", "seaborn", "pydantic"
    ],
    "Cloud & DevOps": [
        "aws", "amazon web services", "gcp", "google cloud platform", "google cloud", "azure", "microsoft azure",
        "docker", "kubernetes", "k8s", "terraform", "ci/cd", "continuous integration", "continuous deployment",
        "github actions", "gitlab ci", "jenkins", "ansible", "helm", "cloudformation", "serverless",
        "lambda", "ec2", "s3", "cloud run", "vertex ai", "iam", "cloudwatch"
    ],
    "Databases & Big Data": [
        "postgresql", "postgres", "mysql", "mongodb", "redis", "elasticsearch", "cassandra",
        "snowflake", "bigquery", "databricks", "apache spark", "spark", "apache kafka", "kafka",
        "apache airflow", "airflow", "dbt", "hadoop", "hive", "dynamodb", "neo4j", "oracle", "sql server"
    ],
    "Architecture & Methodologies": [
        "microservices", "rest api", "restful apis", "rest", "graphql", "grpc", "distributed systems",
        "event-driven architecture", "etl", "elt", "data pipelines", "data warehousing",
        "data modeling", "system design", "agile", "scrum", "kanban", "test-driven development",
        "tdd", "object-oriented programming", "oop", "clean architecture", "acid"
    ],
    "Analytics, BI & AI/ML Tools": [
        "looker", "tableau", "power bi", "excel", "google looker studio", "metabase",
        "llms", "large language models", "rag", "retrieval augmented generation",
        "agentic workflows", "embeddings", "prompt engineering", "nlp", "natural language processing",
        "computer vision", "ab testing", "a/b testing", "data visualization", "statistical analysis",
        "regression", "classification", "clustering", "fine-tuning", "vector databases", "pinecone", "chromadb", "faiss"
    ]
}

# Aliases and canonical normalization
KEYWORD_ALIASES: dict[str, str] = {
    "react.js": "React",
    "reactjs": "React",
    "node": "Node.js",
    "nodejs": "Node.js",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "amazon web services": "AWS",
    "google cloud platform": "GCP",
    "google cloud": "GCP",
    "microsoft azure": "Azure",
    "k8s": "Kubernetes",
    "scikit-learn": "Scikit-Learn",
    "sklearn": "Scikit-Learn",
    "golang": "Go",
    "restful apis": "RESTful APIs",
    "rest apis": "RESTful APIs",
    "rest api": "RESTful APIs",
    "rest": "REST APIs",
    "ci/cd": "CI/CD",
    "large language models": "LLMs",
    "a/b testing": "A/B Testing",
    "ab testing": "A/B Testing",
    "mysql": "MySQL",
    "nosql": "NoSQL",
    "apache spark": "Spark",
    "apache kafka": "Kafka",
    "apache airflow": "Airflow",
}


@dataclass
class KeywordMatchResult:
    """Detailed result of ATS keyword analysis."""
    jd_keywords: list[str] = field(default_factory=list)
    resume_keywords: list[str] = field(default_factory=list)
    matched_keywords: list[str] = field(default_factory=list)
    missing_keywords: list[str] = field(default_factory=list)
    critical_missing: list[str] = field(default_factory=list)
    ats_score: float = 0.0
    passed_90_threshold: bool = False
    keyword_categories: dict[str, list[str]] = field(default_factory=dict)
    keyword_weights: dict[str, float] = field(default_factory=dict)
    keyword_frequencies: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ats_score": round(self.ats_score, 1),
            "passed_90_threshold": self.passed_90_threshold,
            "total_jd_keywords": len(self.jd_keywords),
            "matched_count": len(self.matched_keywords),
            "missing_count": len(self.missing_keywords),
            "matched_keywords": self.matched_keywords,
            "missing_keywords": self.missing_keywords,
            "critical_missing": self.critical_missing,
            "categories": self.keyword_categories,
        }


def canonical_name(kw: str) -> str:
    """Normalize keyword to canonical display form."""
    cleaned = kw.strip()
    lowered = cleaned.lower()
    if lowered in KEYWORD_ALIASES:
        return KEYWORD_ALIASES[lowered]
    # Check taxonomy matching
    for cat, items in TECH_TAXONOMY.items():
        for item in items:
            if lowered == item.lower():
                return item.title() if len(item) > 3 else item.upper()
    return cleaned.title() if len(cleaned) > 4 else cleaned.upper()


def extract_keywords_heuristics(text: str) -> tuple[list[str], dict[str, list[str]], dict[str, int]]:
    """Deterministic extractor for technical keywords using regex word boundary matching."""
    text_lower = " " + text.lower() + " "
    found_keywords: set[str] = set()
    category_map: dict[str, list[str]] = {}
    frequencies: dict[str, int] = {}

    for category, terms in TECH_TAXONOMY.items():
        category_map[category] = []
        for term in terms:
            escaped_term = re.escape(term)
            # Pattern matches terms without alphanumeric boundaries, allowing punctuation (like . or ,) outside
            pattern = rf"(?<![a-zA-Z0-9_]){escaped_term}(?![a-zA-Z0-9_])"
            matches = list(re.finditer(pattern, text_lower))
            if matches:
                canon = canonical_name(term)
                found_keywords.add(canon)
                category_map[category].append(canon)
                frequencies[canon] = len(matches)

    # Sort keywords alphabetically
    sorted_keywords = sorted(list(found_keywords))
    return sorted_keywords, category_map, frequencies


def calculate_ats_match(
    jd_keywords: list[str],
    resume_keywords: list[str],
    critical_keywords: list[str] | None = None
) -> KeywordMatchResult:
    """Calculates weighted ATS keyword match score between JD and Resume.

    Weights:
        Critical JD Keywords: 3.0
        Standard JD Keywords: 1.5
    """
    jd_set = {k.strip().lower() for k in jd_keywords if k.strip()}
    res_set = {k.strip().lower() for k in resume_keywords if k.strip()}
    crit_set = {k.strip().lower() for k in (critical_keywords or []) if k.strip()}

    if not jd_set:
        return KeywordMatchResult(ats_score=100.0, passed_90_threshold=True)

    matched: list[str] = []
    missing: list[str] = []
    critical_missing: list[str] = []
    weights: dict[str, float] = {}

    total_weighted_points = 0.0
    matched_weighted_points = 0.0

    # Build map of lower -> canonical
    jd_canon_map = {k.strip().lower(): k.strip() for k in jd_keywords if k.strip()}

    for kw_low, kw_canon in jd_canon_map.items():
        weight = 3.0 if (kw_low in crit_set or "must" in kw_low) else 1.5
        weights[kw_canon] = weight
        total_weighted_points += weight

        if kw_low in res_set:
            matched.append(kw_canon)
            matched_weighted_points += weight
        else:
            missing.append(kw_canon)
            if kw_low in crit_set:
                critical_missing.append(kw_canon)

    score = (matched_weighted_points / total_weighted_points * 100.0) if total_weighted_points > 0 else 0.0
    score = min(100.0, max(0.0, score))

    matched.sort()
    missing.sort()
    critical_missing.sort()

    return KeywordMatchResult(
        jd_keywords=sorted(list(jd_canon_map.values())),
        resume_keywords=sorted(resume_keywords),
        matched_keywords=matched,
        missing_keywords=missing,
        critical_missing=critical_missing,
        ats_score=round(score, 1),
        passed_90_threshold=(score >= 90.0),
        keyword_weights=weights,
    )
