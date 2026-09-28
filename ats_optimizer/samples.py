"""Realistic sample Job Descriptions and Resume data for testing and demonstration.
"""

from __future__ import annotations

import os
from pathlib import Path

SAMPLE_JOB_DESCRIPTIONS = {
    "Senior Data & Analytics Engineer (SQL, Python, Snowflake, Looker)": """
Role: Senior Data Analytics Engineer
Company: CloudScale Technologies
Location: Hybrid / Remote

About the Role:
We are seeking a high-caliber Data Analytics Engineer to architect our enterprise reporting infrastructure and build scalable data automation pipelines. You will partner with cross-functional product, finance, and engineering leaders to translate complex business requirements into high-performance analytical systems.

Key Responsibilities:
- Design, build, and maintain automated ETL / ELT data pipelines in Python and SQL across Snowflake and BigQuery.
- Architect high-speed SQL queries, stored procedures, and modular data models to optimize database performance across multi-million record datasets.
- Develop interactive executive dashboards and KPI reporting suites in Looker, Tableau, and Power BI.
- Lead A/B testing statistical analyses and customer behavior modeling to guide growth strategy.
- Establish CI/CD deployment standards, data quality monitoring, and automated test-driven development (TDD) for data warehouse pipelines.
- Collaborate with engineering teams in an Agile / Scrum framework to deploy event-driven data streaming pipelines utilizing Docker and Apache Airflow.

Qualifications & Technical Requirements:
- 2+ years of production experience in SQL (MySQL, PostgreSQL, Snowflake) query optimization and schema design.
- Hands-on proficiency in Python (Pandas, NumPy) for data wrangling, automation, and backend pipeline orchestration.
- Proven track record with Looker or Tableau creating reusable data exploration models and business dashboards.
- Experience with cloud platforms: GCP (BigQuery, Cloud Run) or AWS (S3, Redshift, Lambda).
- Familiarity with modern data stack tools: Apache Airflow, dbt, Docker, Git, and CI/CD pipelines.
- Strong grounding in distributed systems concepts, microservices, and RESTful APIs integration.
""",

    "Senior AI & Python Backend Engineer (FastAPI, Docker, Microservices, LLMs)": """
Role: Senior Python / AI Systems Engineer
Company: Apex Intelligent Systems

About the Role:
We are building next-generation agentic AI applications and high-throughput backend services. We need a Senior Python Engineer to design resilient microservices, integrate LLMs and vector search, and build fault-tolerant APIs.

Responsibilities:
- Architect and deploy scalable microservices using Python and FastAPI.
- Build high-concurrency RESTful APIs and asynchronous message queues using Redis and Apache Kafka.
- Design database schemas and query indexing strategies in PostgreSQL and MongoDB.
- Containerize services with Docker and orchestrate workloads on Kubernetes (k8s) in AWS.
- Implement LLM agentic workflows, prompt engineering, RAG pipelines, and vector database embeddings (Pinecone, ChromaDB).
- Enforce rigorous testing (pytest), CI/CD pipelines via GitHub Actions, and system reliability benchmarks.

Technical Requirements:
- Deep expertise in Python 3.10+, FastAPI, and asyncio.
- Strong experience with Docker, Kubernetes, AWS (EC2, S3, CloudWatch), and CI/CD.
- Production experience with PostgreSQL, Redis caching, and REST APIs.
- Familiarity with LLMs, PyTorch, LangChain, or Google GenAI/Antigravity ecosystems.
""",
}

SAMPLE_RESUME_TEXT = """
PRACHI JAIN
Hyderabad, India | +91-6266761271 | prachijain6699@gmail.com
LinkedIn: linkedin.com/in/prachi-jain6584 | GitHub: github.com/PrachiJain123
Immediate Joiner

SUMMARY
Immediate joiner and Data Analytics Specialist with 2+ years of hands-on experience in SQL (MySQL), Python, Looker, and data automation. Skilled in analysing large datasets, developing automation pipelines, building interactive dashboards, and delivering data-driven insights to support business decisions.

SKILLS
- Languages: SQL (MySQL), Python (Pandas, NumPy), Basics of C, C++
- Tools: Looker, Power BI, Advanced Excel, Jupyter Notebook, Git, GitHub
- Concepts: Data Cleaning, Automation, Data Visualization, Problem Solving, Statistical Analysis

EXPERIENCE
Data Analytics Specialist | Tata Consultancy Services (TCS)
Hyderabad, India | July 2022 – Present
- Analyzed large-scale operational datasets using MySQL and Python to extract performance metrics and actionable insights for leadership.
- Designed and maintained automated weekly and monthly executive dashboards in Looker, reducing reporting overhead for business stakeholders.
- Created complex SQL queries, joins, subqueries, and window functions to aggregate customer activity data across diverse source tables.
- Collaborated with engineering teams to identify data anomalies and validate ETL consistency across production databases.
- Automated data processing routines in Python using Pandas, cutting down manual data preparation time significantly.

PROJECTS
- Customer Churn Predictive Analysis: Developed analytical model in Python using Pandas and Scikit-Learn to evaluate customer churn trends, presenting findings via interactive visualization dashboards.
- Sales Performance Pipeline: Built end-to-end data pipeline extracting transaction records from MySQL database and displaying real-time revenue KPIs in Looker.

EDUCATION
- Bachelor of Technology (B.Tech) in Computer Science & Engineering
- Rajiv Gandhi Proudyogiki Vishwavidyalaya (RGPV) | 2018 – 2022
"""


def get_default_resume_text() -> str:
    """Loads Prachi_Jain_Resume.pdf from workspace if present, else fallback sample."""
    workspace_pdf = Path("Prachi_Jain_Resume.pdf")
    if workspace_pdf.is_file():
        try:
            from .parser import extract_text_from_pdf
            extracted = extract_text_from_pdf(workspace_pdf)
            if extracted and len(extracted) > 100:
                return extracted
        except Exception:
            pass
    return SAMPLE_RESUME_TEXT
