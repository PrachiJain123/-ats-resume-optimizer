# 🚀 ATS Resume Optimizer (Antigravity SDK & Gemini 3.1 Pro)

An enterprise-grade AI resume optimization engine that takes a **Job Description** and **Resume**, extracts technical competencies, rewrites experience bullets using Google's **XYZ Formula**, and executes an automated optimization loop to guarantee a **90%+ ATS Keyword Match**.

---

## 🌟 Key Capabilities

1. **Antigravity SDK & Gemini 3.1 Pro Integration**:
   - Programmatically orchestrates agents using `google.antigravity.Agent` configured with `LocalAgentConfig(model="gemini-3.1-pro")`.
   - Dual-mode execution: Live Gemini 3.1 Pro AI extraction + High-fidelity offline heuristic fallback.

2. **Technical Keyword Extraction & Taxonomy Categorization**:
   - Parses technical terms across 6 domains:
     - *Core Languages & Querying* (Python, SQL, C++, Java, etc.)
     - *Frameworks & Libraries* (Pandas, PyTorch, FastAPI, React, etc.)
     - *Cloud & DevOps* (AWS, GCP, Docker, Kubernetes, CI/CD, etc.)
     - *Databases & Big Data* (PostgreSQL, MySQL, Snowflake, BigQuery, Airflow, etc.)
     - *Architecture & Methodologies* (Microservices, RESTful APIs, Distributed Systems, Agile)
     - *Tools & Analytical Platforms* (Looker, Tableau, Power BI, A/B Testing, etc.)
   - Identifies candidate's skills gap against Job Description requirements.

3. **Google XYZ Formula Bullet Rewriting**:
   - Strictly reformulates experience bullet points into:
     $$\textbf{"Accomplished [X] as measured by [Y], by doing [Z]"}$$
   - **[X] Accomplished**: Active leadership verb + quantified business/technical impact.
   - **[Y] Measured by**: Explicit benchmark, metric, latency reduction, throughput, or dollar cost savings.
   - **[Z] By doing**: Implementation techniques, architecture patterns, and infused target keywords.

4. **Guaranteed 90%+ ATS Match Check & Optimization Loop**:
   - Computes weighted ATS match score:
     $$\text{ATS Score} = \frac{\sum_{k \in \text{Matched}} w_k}{\sum_{k \in \text{All JD Keywords}} w_k} \times 100$$
   - Evaluates initial baseline score vs post-rewriting score.
   - Automatically initiates the ATS Boost cycle until the score exceeds **90.0%**.

5. **Multi-Format Export**:
   - **Formatted Markdown Resume** (`resume_optimized.md`)
   - **ATS-Compliant HTML Document** (`resume_optimized.html`) with print-to-PDF styles.
   - **Full ATS Audit Report** (`ats_audit_report.md` & `ats_report.json`).

---

## 📂 Project Architecture

```text
project_after_uber/
├── app.py                      # Interactive Streamlit Web Dashboard
├── cli.py                      # Full-featured Command-Line Interface
├── test_ats_optimizer.py       # Automated unit test suite (8 tests)
├── requirements.txt            # Dependency specifications
├── output/                     # Generated resumes, reports, and JSON data
│   ├── resume_optimized.md     # Tailored markdown resume
│   ├── resume_optimized.html   # Clean, ATS-compliant HTML (Print to PDF)
│   ├── ats_audit_report.md     # Detailed keyword and XYZ audit report
│   └── ats_report.json         # Structured audit data
└── ats_optimizer/              # Core modular engine
    ├── __init__.py
    ├── config.py               # Model config ('gemini-3.1-pro') & API key management
    ├── client.py               # Antigravity SDK Agent wrapper for Gemini 3.1 Pro
    ├── parser.py               # PDF parser (PyMuPDF) and section extractor
    ├── keyword_engine.py       # Tech taxonomy & weighted ATS scoring
    ├── xyz_rewriter.py         # Google XYZ bullet transformation engine
    ├── ats_matcher.py          # 90+ ATS verification and boost loop
    ├── formatter.py            # Markdown, HTML, and JSON report generator
    └── samples.py              # Pre-loaded JDs & resume fixtures
```

---

## ⚡ Quick Start

### 1. Run the Web Dashboard
```bash
streamlit run app.py
```
- Open `http://localhost:8501` in your browser.
- Upload a resume PDF (or paste text) and target Job Description.
- View live before/after bullet cards, keyword match metrics, and download optimized resumes with 1 click!

### 2. Run via Command Line (CLI)

#### Run with sample data (Senior Data Analyst JD + Workspace Resume):
```bash
python cli.py --sample
```

#### Run with your custom files:
```bash
python cli.py --jd path/to/job_description.txt --resume path/to/resume.pdf --output-dir ./output
```

### 3. Run Automated Tests
```bash
python test_ats_optimizer.py
```

---

## 🔑 Gemini API Key Configuration

To enable live generation with **Gemini 3.1 Pro**:
- Set an environment variable:
  ```powershell
  $env:GEMINI_API_KEY = "your-gemini-api-key-here"
  ```
- Or enter it directly in the Streamlit web dashboard sidebar and click **Save Key**.
- If no key is set, the application automatically runs in High-Fidelity Heuristic Optimization mode without crashing.
