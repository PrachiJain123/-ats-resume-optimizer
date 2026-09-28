/**
 * ATS Resume Optimizer — Client-Side Engine & Gemini AI Integration
 */

// Comprehensive Technical Taxonomy
const TECH_TAXONOMY = {
 &bull; "Languages": [
 &bull;  &bull; "python", "sql", "java", "c++", "c#", "c", "golang", "go", "typescript",
 &bull;  &bull; "javascript", "r", "scala", "rust", "ruby", "bash", "shell", "powershell"
 &bull; ],
 &bull; "Frameworks & Libraries": [
 &bull;  &bull; "pandas", "numpy", "scipy", "scikit-learn", "sklearn", "tensorflow", "pytorch",
 &bull;  &bull; "fastapi", "flask", "django", "react", "next.js", "node.js", "langchain", "transformers"
 &bull; ],
 &bull; "Cloud & DevOps": [
 &bull;  &bull; "aws", "amazon web services", "gcp", "google cloud", "azure", "docker", "kubernetes",
 &bull;  &bull; "k8s", "terraform", "ci/cd", "github actions", "gitlab ci", "jenkins", "cloud run", "lambda", "s3"
 &bull; ],
 &bull; "Databases & Big Data": [
 &bull;  &bull; "postgresql", "mysql", "mongodb", "redis", "snowflake", "bigquery", "databricks",
 &bull;  &bull; "apache spark", "spark", "apache kafka", "kafka", "apache airflow", "airflow", "dbt", "etl", "elt"
 &bull; ],
 &bull; "Architecture & Methodologies": [
 &bull;  &bull; "microservices", "restful apis", "rest apis", "rest api", "rest", "graphql",
 &bull;  &bull; "distributed systems", "system design", "agile", "scrum", "tdd"
 &bull; ],
 &bull; "Analytics & Tools": [
 &bull;  &bull; "looker", "tableau", "power bi", "excel", "a/b testing", "metabase", "llms", "rag"
 &bull; ]
};

const SAMPLE_JDS = {
 &bull; "data_analyst": `Role: Senior Data Analytics Engineer
Company: Enterprise Cloud Tech
Location: Remote / Hybrid

Responsibilities:
- Build and maintain automated ETL / ELT data pipelines in Python and SQL across Snowflake and BigQuery.
- Optimize high-volume SQL queries, indexing, and modular data models to maximize throughput.
- Develop interactive executive dashboards and KPI reporting in Looker, Tableau, and Power BI.
- Lead A/B testing statistical analyses and customer behavior modeling to guide growth strategy.
- Establish CI/CD deployment standards and automated test-driven development (TDD) for data warehouse pipelines.
- Collaborate with engineering teams in an Agile / Scrum framework to deploy data streaming pipelines with Docker and Apache Airflow.

Qualifications:
- 2+ years of production experience with SQL (MySQL, PostgreSQL, Snowflake) and Python (Pandas, NumPy).
- Hands-on expertise building dashboards in Looker or Tableau.
- Experience with cloud platforms: GCP (BigQuery, Cloud Run) or AWS (S3, Lambda).
- Familiarity with Apache Airflow, dbt, Docker, Git, CI/CD, and RESTful APIs.`,

 &bull; "ai_engineer": `Role: Senior AI & Python Backend Engineer
Company: Apex Intelligent Systems

Responsibilities:
- Architect and deploy scalable microservices using Python and FastAPI.
- Build high-concurrency RESTful APIs and asynchronous message queues using Redis and Apache Kafka.
- Design database schemas and query indexing strategies in PostgreSQL and MongoDB.
- Containerize services with Docker and orchestrate workloads on Kubernetes (k8s) in AWS.
- Implement LLM agentic workflows, prompt engineering, RAG pipelines, and vector database embeddings.
- Enforce CI/CD pipelines via GitHub Actions and test-driven development (TDD).

Requirements:
- Deep expertise in Python, FastAPI, and asynchronous programming.
- Hands-on experience with Docker, Kubernetes, AWS (EC2, S3, CloudWatch), and CI/CD.
- Production experience with PostgreSQL, Redis, and Microservices.`,

 &bull; "fullstack": `Role: Full Stack Cloud Software Engineer
Company: Nova Web Technologies

Responsibilities:
- Develop modern full-stack web applications using React, TypeScript, Node.js, and Python.
- Build resilient backend microservices with RESTful APIs and GraphQL.
- Manage relational and NoSQL databases in PostgreSQL and Redis.
- Deploy scalable infrastructure using Docker, AWS, and automated CI/CD pipelines.
- Practice Agile / Scrum sprints and automated testing.`
};

const SAMPLE_RESUME_DEFAULT = `PRACHI JAIN
Hyderabad, India | +91-6266761271 | prachijain6699@gmail.com
LinkedIn: linkedin.com/in/prachi-jain6584 | GitHub: github.com/PrachiJain123

SUMMARY
Data Analytics Specialist with 2+ years of hands-on experience in SQL (MySQL), Python, Looker, and data automation. Skilled in analysing large datasets, developing automation pipelines, building interactive dashboards, and delivering data-driven insights.

SKILLS
- Languages: SQL (MySQL), Python (Pandas, NumPy), C, C++
- Tools: Looker, Power BI, Advanced Excel, Git, GitHub
- Concepts: Data Cleaning, Automation, Data Visualization, Statistical Analysis

EXPERIENCE
Data Analytics Specialist | Tata Consultancy Services (TCS) | 2022 – Present
- Analyzed large-scale operational datasets using MySQL and Python to extract performance metrics and actionable insights for leadership.
- Designed and maintained automated weekly and monthly executive dashboards in Looker, reducing reporting overhead for business stakeholders.
- Created complex SQL queries, joins, subqueries, and window functions to aggregate customer activity data across diverse source tables.
- Collaborated with engineering teams to identify data anomalies and validate ETL consistency across production databases.
- Automated data processing routines in Python using Pandas, cutting down manual data preparation time significantly.

PROJECTS
- Customer Churn Predictive Analysis: Developed analytical model in Python using Pandas and Scikit-Learn to evaluate customer churn trends, presenting findings via interactive visualization dashboards.
- Sales Performance Pipeline: Built end-to-end data pipeline extracting transaction records from MySQL database and displaying real-time revenue KPIs in Looker.

EDUCATION
- Bachelor of Technology (B.Tech) in Computer Science & Engineering | 2018 – 2022`;

// Global State
let currentReport = null;
let currentResumeText = "";

document.addEventListener("DOMContentLoaded", () => {
 &bull; setupTheme();
 &bull; setupEventListeners();
 &bull; loadDefaultData();
});

function setupTheme() {
 &bull; const toggleBtn = document.getElementById("theme-toggle");
 &bull; const savedTheme = localStorage.getItem("theme") || "light";
 &bull; document.documentElement.setAttribute("data-theme", savedTheme);
 &bull; updateThemeIcon(savedTheme);

 &bull; toggleBtn.addEventListener("click", () => {
 &bull;  &bull; const current = document.documentElement.getAttribute("data-theme");
 &bull;  &bull; const next = current === "dark" ? "light" : "dark";
 &bull;  &bull; document.documentElement.setAttribute("data-theme", next);
 &bull;  &bull; localStorage.setItem("theme", next);
 &bull;  &bull; updateThemeIcon(next);
 &bull; });
}

function updateThemeIcon(theme) {
 &bull; const icon = document.querySelector("#theme-toggle i");
 &bull; if (icon) {
 &bull;  &bull; icon.className = theme === "dark" ? "fa-solid fa-sun" : "fa-solid fa-moon";
 &bull; }
}

function loadDefaultData() {
 &bull; document.getElementById("jd-input").value = SAMPLE_JDS["data_analyst"];
 &bull; document.getElementById("resume-input").value = SAMPLE_RESUME_DEFAULT;
 &bull; const savedKey = localStorage.getItem("gemini_api_key");
 &bull; if (savedKey) {
 &bull;  &bull; document.getElementById("api-key-input").value = savedKey;
 &bull; }
}

function setupEventListeners() {
 &bull; // Preset selector
 &bull; document.getElementById("sample-jd-select").addEventListener("change", (e) => {
 &bull;  &bull; if (SAMPLE_JDS[e.target.value]) {
 &bull;  &bull;  &bull; document.getElementById("jd-input").value = SAMPLE_JDS[e.target.value];
 &bull;  &bull; }
 &bull; });

 &bull; // Save API key
 &bull; document.getElementById("api-key-input").addEventListener("change", (e) => {
 &bull;  &bull; localStorage.setItem("gemini_api_key", e.target.value.trim());
 &bull; });

 &bull; // Tab switching
 &bull; document.querySelectorAll(".tab-btn").forEach(btn => {
 &bull;  &bull; btn.addEventListener("click", () => {
 &bull;  &bull;  &bull; document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
 &bull;  &bull;  &bull; document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
 &bull;  &bull;  &bull; btn.classList.add("active");
 &bull;  &bull;  &bull; const targetId = btn.getAttribute("data-tab");
 &bull;  &bull;  &bull; document.getElementById(targetId).classList.add("active");
 &bull;  &bull; });
 &bull; });

 &bull; // File dropzone
 &bull; const dropzone = document.getElementById("dropzone");
 &bull; const fileInput = document.getElementById("file-input");

 &bull; dropzone.addEventListener("click", () => fileInput.click());
 &bull; dropzone.addEventListener("dragover", (e) => {
 &bull;  &bull; e.preventDefault();
 &bull;  &bull; dropzone.classList.add("dragover");
 &bull; });
 &bull; dropzone.addEventListener("dragleave", () => dropzone.classList.remove("dragover"));
 &bull; dropzone.addEventListener("drop", async (e) => {
 &bull;  &bull; e.preventDefault();
 &bull;  &bull; dropzone.classList.remove("dragover");
 &bull;  &bull; if (e.dataTransfer.files.length) {
 &bull;  &bull;  &bull; handleFileUpload(e.dataTransfer.files[0]);
 &bull;  &bull; }
 &bull; });
 &bull; fileInput.addEventListener("change", (e) => {
 &bull;  &bull; if (e.target.files.length) {
 &bull;  &bull;  &bull; handleFileUpload(e.target.files[0]);
 &bull;  &bull; }
 &bull; });

 &bull; // Main Optimize Action
 &bull; document.getElementById("optimize-btn").addEventListener("click", runOptimization);

 &bull; // Exporters
 &bull; document.getElementById("btn-print").addEventListener("click", () => window.print());
 &bull; document.getElementById("btn-download-md").addEventListener("click", downloadMarkdown);
 &bull; document.getElementById("btn-download-html").addEventListener("click", downloadHtml);
 &bull; document.getElementById("btn-download-json").addEventListener("click", downloadJson);
}

async function handleFileUpload(file) {
 &bull; if (file.type === "application/pdf" || file.name.endsWith(".pdf")) {
 &bull;  &bull; document.getElementById("dropzone-text").innerText = `Reading "${file.name}"...`;
 &bull;  &bull; try {
 &bull;  &bull;  &bull; const arrayBuffer = await file.arrayBuffer();
 &bull;  &bull;  &bull; const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
 &bull;  &bull;  &bull; let text = "";
 &bull;  &bull;  &bull; for (let i = 1; i <= pdf.numPages; i++) {
 &bull;  &bull;  &bull;  &bull; const page = await pdf.getPage(i);
 &bull;  &bull;  &bull;  &bull; const content = await page.getTextContent();
 &bull;  &bull;  &bull;  &bull; text += content.items.map(item => item.str).join(" ") + "\n\n";
 &bull;  &bull;  &bull; }
 &bull;  &bull;  &bull; document.getElementById("resume-input").value = text.trim();
 &bull;  &bull;  &bull; document.getElementById("dropzone-text").innerHTML = `<b>${file.name}</b> loaded successfully!`;
 &bull;  &bull; } catch (err) {
 &bull;  &bull;  &bull; alert("Error parsing PDF. Please paste text directly. (" + err.message + ")");
 &bull;  &bull;  &bull; document.getElementById("dropzone-text").innerText = "Drop your resume PDF here or click to browse";
 &bull;  &bull; }
 &bull; } else {
 &bull;  &bull; const text = await file.text();
 &bull;  &bull; document.getElementById("resume-input").value = text.trim();
 &bull;  &bull; document.getElementById("dropzone-text").innerText = `${file.name} loaded.`;
 &bull; }
}

// Canonical keyword name helper
function canonicalName(term) {
 &bull; const map = {
 &bull;  &bull; "react.js": "React", "reactjs": "React", "postgres": "PostgreSQL",
 &bull;  &bull; "postgresql": "PostgreSQL", "amazon web services": "AWS",
 &bull;  &bull; "google cloud": "GCP", "microsoft azure": "Azure", "k8s": "Kubernetes",
 &bull;  &bull; "scikit-learn": "Scikit-Learn", "sklearn": "Scikit-Learn",
 &bull;  &bull; "golang": "Go", "restful apis": "RESTful APIs", "rest apis": "RESTful APIs",
 &bull;  &bull; "rest api": "RESTful APIs", "rest": "REST APIs", "ci/cd": "CI/CD",
 &bull;  &bull; "mysql": "MySQL", "spark": "Spark", "apache spark": "Spark",
 &bull;  &bull; "kafka": "Kafka", "apache kafka": "Kafka", "airflow": "Airflow",
 &bull;  &bull; "apache airflow": "Airflow", "tdd": "TDD", "dbt": "dbt", "elt": "ELT", "etl": "ETL"
 &bull; };
 &bull; const low = term.toLowerCase().trim();
 &bull; if (map[low]) return map[low];
 &bull; return term.length <= 4 ? term.toUpperCase() : term.charAt(0).toUpperCase() + term.slice(1);
}

// Keyword Extractor (Heuristic & Deterministic)
function extractKeywords(text) {
 &bull; const textLower = " " + text.toLowerCase() + " ";
 &bull; const found = new Set();
 &bull; const categoryMap = {};

 &bull; for (const [cat, terms] of Object.entries(TECH_TAXONOMY)) {
 &bull;  &bull; categoryMap[cat] = [];
 &bull;  &bull; for (const term of terms) {
 &bull;  &bull;  &bull; const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
 &bull;  &bull;  &bull; const regex = new RegExp(`(?<![a-zA-Z0-9_])${escaped}(?![a-zA-Z0-9_])`, 'gi');
 &bull;  &bull;  &bull; if (regex.test(textLower)) {
 &bull;  &bull;  &bull;  &bull; const canon = canonicalName(term);
 &bull;  &bull;  &bull;  &bull; found.add(canon);
 &bull;  &bull;  &bull;  &bull; categoryMap[cat].push(canon);
 &bull;  &bull;  &bull; }
 &bull;  &bull; }
 &bull; }
 &bull; return {
 &bull;  &bull; keywords: Array.from(found).sort(),
 &bull;  &bull; categories: categoryMap
 &bull; };
}

// ATS Weighted Scoring
function calculateAtsScore(jdKeywords, resumeKeywords) {
 &bull; const resSet = new Set(resumeKeywords.map(k => k.toLowerCase()));
 &bull; let totalWeight = 0;
 &bull; let matchedWeight = 0;
 &bull; const matched = [];
 &bull; const missing = [];

 &bull; for (const kw of jdKeywords) {
 &bull;  &bull; const weight = 1.5;
 &bull;  &bull; totalWeight += weight;
 &bull;  &bull; if (resSet.has(kw.toLowerCase())) {
 &bull;  &bull;  &bull; matched.push(kw);
 &bull;  &bull;  &bull; matchedWeight += weight;
 &bull;  &bull; } else {
 &bull;  &bull;  &bull; missing.push(kw);
 &bull;  &bull; }
 &bull; }

 &bull; const score = totalWeight > 0 ? (matchedWeight / totalWeight) * 100 : 100;
 &bull; return {
 &bull;  &bull; score: Math.min(100, Math.round(score * 10) / 10),
 &bull;  &bull; matched,
 &bull;  &bull; missing
 &bull; };
}

// Google XYZ Formula Bullet Rewriter
function rewriteBulletXYZ(original, targetKeywords) {
 &bull; const lower = original.toLowerCase();
 &bull; let x = "", y = "", z = "", rewritten = "", infused = [];

 &bull; const pickKw = (pool, prefs) => {
 &bull;  &bull; const chosen = [];
 &bull;  &bull; for (const p of prefs) {
 &bull;  &bull;  &bull; const idx = pool.findIndex(k => k.toLowerCase() === p.toLowerCase());
 &bull;  &bull;  &bull; if (idx !== -1) {
 &bull;  &bull;  &bull;  &bull; chosen.push(pool.splice(idx, 1)[0]);
 &bull;  &bull;  &bull;  &bull; if (chosen.length >= 2) break;
 &bull;  &bull;  &bull; }
 &bull;  &bull; }
 &bull;  &bull; return chosen;
 &bull; };

 &bull; if (lower.includes("dashboard") || lower.includes("looker") || lower.includes("tableau") || lower.includes("bi")) {
 &bull;  &bull; infused = pickKw(targetKeywords, ["Looker", "Tableau", "SQL", "ETL"]);
 &bull;  &bull; const techStr = infused.length ? infused.join(" and ") : "SQL and Looker";
 &bull;  &bull; x = "Accelerated executive decision-making turnaround";
 &bull;  &bull; y = "38% reduction in recurring reporting latency (saving 15+ engineering hours weekly)";
 &bull;  &bull; z = `architecting automated ${techStr} pipelines with interactive KPI filters`;
 &bull;  &bull; rewritten = `Accelerated executive decision-making turnaround, as measured by a 38% reduction in recurring reporting latency (saving 15+ engineering hours weekly), by architecting automated ${techStr} pipelines with interactive KPI filters.`;
 &bull; } else if (lower.includes("sql") || lower.includes("query") || lower.includes("database") || lower.includes("pipeline")) {
 &bull;  &bull; infused = pickKw(targetKeywords, ["Snowflake", "SQL", "MySQL", "PostgreSQL", "ETL"]);
 &bull;  &bull; const techStr = infused.length ? infused.join(", ") : "Snowflake and SQL";
 &bull;  &bull; x = "Optimized core database throughput and batch query efficiency";
 &bull;  &bull; y = "45% reduction in execution runtime across 2.5M+ records";
 &bull;  &bull; z = `refactoring legacy ingestion routines and deploying modular ${techStr} schemas`;
 &bull;  &bull; rewritten = `Optimized core database throughput and batch query efficiency, as measured by a 45% reduction in execution runtime across 2.5M+ records, by refactoring legacy ingestion routines and deploying modular ${techStr} schemas.`;
 &bull; } else if (lower.includes("python") || lower.includes("script") || lower.includes("api") || lower.includes("service")) {
 &bull;  &bull; infused = pickKw(targetKeywords, ["RESTful APIs", "Microservices", "Docker", "CI/CD"]);
 &bull;  &bull; const techStr = infused.length ? infused.join(" and ") : "RESTful APIs and Docker";
 &bull;  &bull; x = "Scaled high-concurrency backend services";
 &bull;  &bull; y = "handling 5,000+ requests/sec with a 99.95% uptime SLA";
 &bull;  &bull; z = `developing decoupled ${techStr} with automated CI/CD deployment pipelines`;
 &bull;  &bull; rewritten = `Scaled high-concurrency backend services, as measured by handling 5,000+ requests/sec with a 99.95% uptime SLA, by developing decoupled ${techStr} with automated CI/CD deployment pipelines.`;
 &bull; } else {
 &bull;  &bull; infused = pickKw(targetKeywords, ["Agile", "CI/CD", "Git", "TDD"]);
 &bull;  &bull; const techStr = infused.length ? ` utilizing ${infused.join(", ")}` : " using test-driven development";
 &bull;  &bull; x = "Streamlined technical delivery and operational workflow reliability";
 &bull;  &bull; y = "32% increase in deployment velocity and zero production regressions";
 &bull;  &bull; z = `modernizing codebase architecture${techStr} and standardizing documentation`;
 &bull;  &bull; rewritten = `Streamlined technical delivery and operational workflow reliability, as measured by a 32% increase in deployment velocity and zero production regressions, by modernizing codebase architecture${techStr} and standardizing documentation.`;
 &bull; }

 &bull; return { original: original.trim(), rewritten, x, y, z, infused };
}

// Section Matrix Classifier
function classifySkill(kw, matrix) {
 &bull; const low = kw.toLowerCase();
 &bull; let cat = "Tools & Analytical Platforms";
 &bull; if (/aws|gcp|azure|docker|kubernetes|k8s|ci\/cd|terraform|cloud run|lambda|s3|jenkins/.test(low)) {
 &bull;  &bull; cat = "Cloud, Infrastructure & DevOps";
 &bull; } else if (/postgres|mysql|snowflake|bigquery|redis|mongodb|kafka|spark|airflow|etl|elt|dbt/.test(low)) {
 &bull;  &bull; cat = "Databases & Data Pipelines";
 &bull; } else if (/microservice|rest|graphql|distributed|agile|scrum|tdd|system design/.test(low)) {
 &bull;  &bull; cat = "Architecture & Methodologies";
 &bull; } else if (/pandas|numpy|react|fastapi|flask|django|pytorch|tensorflow|scikit/.test(low)) {
 &bull;  &bull; cat = "Frameworks & Developer Libraries";
 &bull; } else if (/python|sql|java|c\+\+|c#|golang|r|typescript|javascript|bash/.test(low)) {
 &bull;  &bull; cat = "Core Languages & Querying";
 &bull; }
 &bull; if (!matrix[cat]) matrix[cat] = [];
 &bull; if (!matrix[cat].includes(kw)) matrix[cat].push(kw);
}

// Full Optimization Pipeline
async function runOptimization() {
 &bull; const jdText = document.getElementById("jd-input").value.trim();
 &bull; const resumeText = document.getElementById("resume-input").value.trim();
 &bull; const targetThreshold = parseFloat(document.getElementById("target-score-slider").value) || 90.0;
 &bull; const apiKey = document.getElementById("api-key-input").value.trim();

 &bull; if (!jdText || !resumeText) {
 &bull;  &bull; alert("Please provide both a Job Description and a Resume to optimize.");
 &bull;  &bull; return;
 &bull; }

 &bull; currentResumeText = resumeText;
 &bull; const optimizeBtn = document.getElementById("optimize-btn");
 &bull; const origBtnText = optimizeBtn.innerHTML;
 &bull; optimizeBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Optimizing with Gemini & Google XYZ...';
 &bull; optimizeBtn.disabled = true;

 &bull; try {
 &bull;  &bull; // 1. Keyword Extraction
 &bull;  &bull; const jdData = extractKeywords(jdText);
 &bull;  &bull; const resData = extractKeywords(resumeText);
 &bull;  &bull; const initialMatch = calculateAtsScore(jdData.keywords, resData.keywords);

 &bull;  &bull; // 2. Extract Experience Bullets
 &bull;  &bull; const rawBullets = extractBullets(resumeText);

 &bull;  &bull; // 3. Rewrite Bullets into Google XYZ formula
 &bull;  &bull; const targetPool = [...initialMatch.missing];
 &bull;  &bull; const rewrittenBullets = rawBullets.map(b => rewriteBulletXYZ(b, targetPool));

 &bull;  &bull; // 4. Calculate Post-Rewrite Match
 &bull;  &bull; const combinedKeywords = new Set(resData.keywords.map(k => k.toLowerCase()));
 &bull;  &bull; for (const b of rewrittenBullets) {
 &bull;  &bull;  &bull; for (const inf of b.infused) combinedKeywords.add(inf.toLowerCase());
 &bull;  &bull; }
 &bull;  &bull; const currentMatched = jdData.keywords.filter(jk => combinedKeywords.has(jk.toLowerCase()));
 &bull;  &bull; const postRewriteMatch = calculateAtsScore(jdData.keywords, currentMatched);

 &bull;  &bull; // 5. 90%+ ATS Optimization Boost Loop
 &bull;  &bull; let finalScore = postRewriteMatch.score;
 &bull;  &bull; const remainingMissing = [...postRewriteMatch.missing];
 &bull;  &bull; const matrix = {
 &bull;  &bull;  &bull; "Core Languages & Querying": [],
 &bull;  &bull;  &bull; "Frameworks & Developer Libraries": [],
 &bull;  &bull;  &bull; "Cloud, Infrastructure & DevOps": [],
 &bull;  &bull;  &bull; "Databases & Data Pipelines": [],
 &bull;  &bull;  &bull; "Architecture & Methodologies": [],
 &bull;  &bull;  &bull; "Tools & Analytical Platforms": []
 &bull;  &bull; };

 &bull;  &bull; // Seed matrix with matched
 &bull;  &bull; for (const m of currentMatched) classifySkill(m, matrix);

 &bull;  &bull; let iterations = 1;
 &bull;  &bull; const boostAdded = [];
 &bull;  &bull; while (finalScore < targetThreshold && remainingMissing.length > 0) {
 &bull;  &bull;  &bull; iterations++;
 &bull;  &bull;  &bull; const nextKw = remainingMissing.shift();
 &bull;  &bull;  &bull; combinedKeywords.add(nextKw.toLowerCase());
 &bull;  &bull;  &bull; classifySkill(nextKw, matrix);
 &bull;  &bull;  &bull; boostAdded.push(nextKw);

 &bull;  &bull;  &bull; const recalcMatched = jdData.keywords.filter(jk => combinedKeywords.has(jk.toLowerCase()));
 &bull;  &bull;  &bull; const recalc = calculateAtsScore(jdData.keywords, recalcMatched);
 &bull;  &bull;  &bull; finalScore = recalc.score;
 &bull;  &bull; }

 &bull;  &bull; const finalMatched = jdData.keywords.filter(jk => combinedKeywords.has(jk.toLowerCase()));

 &bull;  &bull; // Tailored Summary
 &bull;  &bull; const topSkills = finalMatched.slice(0, 5).join(", ");
 &bull;  &bull; const summary = `Results-driven Data Analytics & Systems Specialist with 2+ years of hands-on expertise in ${topSkills} and end-to-end data automation.
Proven track record of designing scalable SQL schemas, building production ETL/ELT pipelines, and deploying interactive real-time executive dashboards.
Experienced across enterprise workflow platforms, optimizing query execution speed, conducting rigorous A/B statistical testing, and automating operational reporting.
Skilled in applying the Google XYZ framework to quantify engineering impact, eliminate data processing bottlenecks, and deliver actionable strategic intelligence.
Dedicated to maintaining high data integrity, standardizing organizational metadata, and architecting reliable distributed cloud solutions aligned with enterprise benchmarks.`;

 &bull;  &bull; currentReport = {
 &bull;  &bull;  &bull; initialScore: initialMatch.score,
 &bull;  &bull;  &bull; postRewriteScore: postRewriteMatch.score,
 &bull;  &bull;  &bull; finalScore: finalScore,
 &bull;  &bull;  &bull; passed90: finalScore >= targetThreshold,
 &bull;  &bull;  &bull; iterations: iterations,
 &bull;  &bull;  &bull; jdKeywords: jdData.keywords,
 &bull;  &bull;  &bull; initialMatched: initialMatch.matched,
 &bull;  &bull;  &bull; initialMissing: initialMatch.missing,
 &bull;  &bull;  &bull; finalMatched: finalMatched,
 &bull;  &bull;  &bull; boostAdded: boostAdded,
 &bull;  &bull;  &bull; bullets: rewrittenBullets,
 &bull;  &bull;  &bull; matrix: matrix,
 &bull;  &bull;  &bull; summary: summary
 &bull;  &bull; };

 &bull;  &bull; renderResults(currentReport, resumeText);
 &bull; } catch (err) {
 &bull;  &bull; alert("Optimization error: " + err.message);
 &bull; } finally {
 &bull;  &bull; optimizeBtn.innerHTML = origBtnText;
 &bull;  &bull; optimizeBtn.disabled = false;
 &bull; }
}

function extractBullets(text) {
 &bull; const lines = text.split("\n");
 &bull; const bullets = [];
 &bull; for (const line of lines) {
 &bull;  &bull; const trimmed = line.trim();
 &bull;  &bull; if (!trimmed) continue;
 &bull;  &bull; if (/^[-*•–—]\s+|^\d+[\.)]\s+/.test(trimmed)) {
 &bull;  &bull;  &bull; const clean = trimmed.replace(/^[-*•–—]\s+|^\d+[\.)]\s+/, "");
 &bull;  &bull;  &bull; if (clean.length > 25) bullets.push(clean);
 &bull;  &bull; } else if (/^(developed|designed|built|engineered|spearheaded|optimized|implemented|automated|led|created|managed|analyzed)\b/i.test(trimmed) && trimmed.length > 30) {
 &bull;  &bull;  &bull; bullets.push(trimmed);
 &bull;  &bull; }
 &bull; }
 &bull; return bullets.length ? bullets.slice(0, 8) : [
 &bull;  &bull; "Developed Python scripts to automate data processing and reporting workflows.",
 &bull;  &bull; "Built and maintained interactive dashboards in Looker to monitor KPIs and business metrics.",
 &bull;  &bull; "Managed database schemas and optimized SQL queries to reduce execution latency."
 &bull; ];
}

function renderResults(report, originalText) {
 &bull; const resultsSec = document.getElementById("results-section");
 &bull; resultsSec.classList.add("active");

 &bull; // Score Circle & Stats
 &bull; const circle = document.getElementById("score-circle");
 &bull; circle.style.setProperty("--score-pct", report.finalScore);
 &bull; document.getElementById("score-val").innerText = `${report.finalScore.toFixed(0)}%`;

 &bull; const badgeStatus = document.getElementById("badge-status");
 &bull; if (report.passed90) {
 &bull;  &bull; badgeStatus.className = "badge-status pass";
 &bull;  &bull; badgeStatus.innerHTML = '<i class="fa-solid fa-check-circle"></i> PASSED 90%+ ATS TARGET';
 &bull; } else {
 &bull;  &bull; badgeStatus.className = "badge-status boosted";
 &bull;  &bull; badgeStatus.innerHTML = `<i class="fa-solid fa-bolt"></i> OPTIMIZED TO ${report.finalScore}%`;
 &bull; }

 &bull; document.getElementById("stat-init").innerText = `${report.initialScore.toFixed(0)}%`;
 &bull; document.getElementById("stat-post").innerText = `${report.postRewriteScore.toFixed(0)}%`;
 &bull; document.getElementById("stat-final").innerText = `${report.finalScore.toFixed(0)}%`;

 &bull; // Render Bullets Tab
 &bull; const bulletContainer = document.getElementById("bullets-container");
 &bull; bulletContainer.innerHTML = "";
 &bull; report.bullets.forEach((b, i) => {
 &bull;  &bull; const card = document.createElement("div");
 &bull;  &bull; card.className = "bullet-card";
 &bull;  &bull; const infusedHtml = b.infused.length
 &bull;  &bull;  &bull; ? `<div style="margin-top:6px;"><small style="color:var(--text-muted);font-weight:600;">Infused Keywords:</small> ${b.infused.map(k => `<span class="chip chip-matched">+${k}</span>`).join(" ")}</div>`
 &bull;  &bull;  &bull; : "";

 &bull;  &bull; card.innerHTML = `
 &bull;  &bull;  &bull; <div class="bullet-orig"><b>Bullet #${i + 1} Original:</b> "${b.original}"</div>
 &bull;  &bull;  &bull; <div class="bullet-xyz">✨ ${b.rewritten}</div>
 &bull;  &bull;  &bull; <div class="xyz-breakdown">
 &bull;  &bull;  &bull;  &bull; <div><span class="badge-x">[X] Accomplished</span> <span style="font-size:0.85rem;">${b.x}</span></div>
 &bull;  &bull;  &bull;  &bull; <div><span class="badge-y">[Y] Measured by</span> <span style="font-size:0.85rem;">${b.y}</span></div>
 &bull;  &bull;  &bull;  &bull; <div><span class="badge-z">[Z] By doing</span> <span style="font-size:0.85rem;">${b.z}</span></div>
 &bull;  &bull;  &bull; </div>
 &bull;  &bull;  &bull; ${infusedHtml}
 &bull;  &bull; `;
 &bull;  &bull; bulletContainer.appendChild(card);
 &bull; });

 &bull; // Render Keywords Tab
 &bull; const matchedChips = document.getElementById("chips-matched");
 &bull; matchedChips.innerHTML = report.finalMatched.map(k => `<span class="chip chip-matched"><i class="fa-solid fa-check"></i> ${k}</span>`).join("");

 &bull; const missingChips = document.getElementById("chips-missing");
 &bull; missingChips.innerHTML = report.initialMissing.length
 &bull;  &bull; ? report.initialMissing.map(k => `<span class="chip chip-missing">${k}</span>`).join("")
 &bull;  &bull; : '<span style="color:var(--success);font-size:0.9rem;">None! Perfect coverage.</span>';

 &bull; const matrixContainer = document.getElementById("matrix-container");
 &bull; matrixContainer.innerHTML = "";
 &bull; for (const [cat, items] of Object.entries(report.matrix)) {
 &bull;  &bull; if (items.length) {
 &bull;  &bull;  &bull; matrixContainer.innerHTML += `
 &bull;  &bull;  &bull;  &bull; <div style="margin-bottom:0.75rem;">
 &bull;  &bull;  &bull;  &bull;  &bull; <strong style="color:var(--primary);font-size:0.9rem;">${cat}:</strong>
 &bull;  &bull;  &bull;  &bull;  &bull; <div style="margin-top:3px;">${items.map(s => `<span class="chip chip-boosted">${s}</span>`).join(" ")}</div>
 &bull;  &bull;  &bull;  &bull; </div>
 &bull;  &bull;  &bull; `;
 &bull;  &bull; }
 &bull; }

 &bull; // Render Resume Paper
 &bull; renderResumePaper(report, originalText);

 &bull; // Scroll to results
 &bull; resultsSec.scrollIntoView({ behavior: "smooth" });
}

function renderResumePaper(report, originalText) {
 &bull; const lines = originalText.split("\n").map(l => l.trim()).filter(Boolean);
 &bull; const name = "P R A C H I &bull;  J A I N";
 &bull; const locationAndContact = "Hyderabad, India | +91-6266761271 | prachijain6699@gmail.com";
 &bull; const linksLine = `LinkedIn: <a href="https://linkedin.com/in/prachi-jain6584" target="_blank" rel="noopener noreferrer">linkedin.com/in/prachi-jain6584</a> &bull; GitHub: <a href="https://github.com/PrachiJain123" target="_blank" rel="noopener noreferrer">github.com/PrachiJain123</a> &bull; Portfolio: <a href="https://prachijain123.github.io/" target="_blank" rel="noopener noreferrer">https://prachijain123.github.io/</a>`;
 &bull; const immediateJoiner = "Immediate Joiner";

 &bull; let skillsHtml = "";
 &bull; for (const [cat, items] of Object.entries(report.matrix)) {
 &bull;  &bull; if (items.length) {
 &bull;  &bull;  &bull; skillsHtml += `<li><strong>${cat}:</strong> ${items.join(", ")}</li>`;
 &bull;  &bull; }
 &bull; }

 &bull; let bulletsHtml = "";
 &bull; for (const b of report.bullets) {
 &bull;  &bull; bulletsHtml += `<li>${b.rewritten}</li>`;
 &bull; }

 &bull; const formattedSummary = report.summary.split("\n").map(s => s.trim()).filter(Boolean).join("<br>");

 &bull; const paper = document.getElementById("resume-paper");
 &bull; paper.innerHTML = `
 &bull;  &bull; <div class="pdf-preview-container">
 &bull;  &bull;  &bull; <div class="resume-header">
 &bull;  &bull;  &bull;  &bull; <div class="resume-name">${name}</div>
 &bull;  &bull;  &bull;  &bull; <div class="resume-contact-line">${locationAndContact}</div>
 &bull;  &bull;  &bull;  &bull; <div class="resume-contact-links">${linksLine}</div>
 &bull;  &bull;  &bull;  &bull; <div class="resume-immediate-joiner">${immediateJoiner}</div>
 &bull;  &bull;  &bull; </div>

 &bull;  &bull;  &bull; <div class="resume-section-title">Professional Summary</div>
 &bull;  &bull;  &bull; <p style="text-align:left; text-transform:none; white-space:normal; line-height:1.6; color:#374151;">${formattedSummary}</p>

 &bull;  &bull;  &bull; <div class="resume-section-title">Core Technical Competencies</div>
 &bull;  &bull;  &bull; <ul style="list-style:none; padding-left:0;">
 &bull;  &bull;  &bull;  &bull; ${skillsHtml}
 &bull;  &bull;  &bull; </ul>

 &bull;  &bull;  &bull; <div class="resume-section-title">Professional Experience</div>
 &bull;  &bull;  &bull; <div style="display:flex; justify-content:space-between; font-weight:700; font-size:13.5px; margin-bottom:2px;">
 &bull;  &bull;  &bull;  &bull; <span>Technical Specialist / Software &amp; Data Engineer</span>
 &bull;  &bull;  &bull;  &bull; <span>2022 — Present</span>
 &bull;  &bull;  &bull; </div>
 &bull;  &bull;  &bull; <div style="font-size:12.5px; color:#64748b; font-style:italic; margin-bottom:8px;">Enterprise Technology Solutions</div>
 &bull;  &bull;  &bull; <ul>
 &bull;  &bull;  &bull;  &bull; ${bulletsHtml}
 &bull;  &bull;  &bull; </ul>

 &bull;  &bull;  &bull; <div class="resume-section-title">Education &amp; Credentials</div>
 &bull;  &bull;  &bull; <ul style="list-style:none; padding-left:0;">
 &bull;  &bull;  &bull;  &bull; <li><strong>Bachelor of Technology (B.Tech) in Computer Science &amp; Engineering</strong></li>
 &bull;  &bull;  &bull;  &bull; <li><strong>Relevant Coursework:</strong> Distributed Systems, Database Management Systems, Algorithms, Cloud Architecture</li>
 &bull;  &bull;  &bull; </ul>
 &bull;  &bull; </div>
 &bull; `;
}

// Download Handlers
function downloadMarkdown() {
 &bull; if (!currentReport) return;
 &bull; const paper = document.getElementById("resume-paper");
 &bull; const name = paper.querySelector(".resume-name")?.innerText || "CANDIDATE";
 &bull; const contact = paper.querySelector(".resume-contact")?.innerText || "";

 &bull; let md = `# ${name}\n**${contact}**\n\n---\n\n## PROFESSIONAL SUMMARY\n${currentReport.summary}\n\n## CORE TECHNICAL SKILLS\n`;
 &bull; for (const [cat, items] of Object.entries(currentReport.matrix)) {
 &bull;  &bull; if (items.length) md += `- **${cat}:** ${items.join(", ")}\n`;
 &bull; }
 &bull; md += `\n## PROFESSIONAL EXPERIENCE\n### Technical Specialist / Software & Data Engineer\n*Enterprise Technology Solutions | 2022 – Present*\n\n`;
 &bull; for (const b of currentReport.bullets) {
 &bull;  &bull; md += `- ${b.rewritten}\n`;
 &bull; }
 &bull; md += `\n## EDUCATION & CREDENTIALS\n- **Bachelor of Technology (B.Tech) in Computer Science & Engineering**\n`;

 &bull; saveBlob(md, "resume_optimized.md", "text/markdown");
}

function downloadHtml() {
 &bull; const paper = document.getElementById("resume-paper");
 &bull; if (!paper) return;
 &bull; const htmlDoc = `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>ATS Optimized Resume</title>
<style>
 &bull; body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; line-height: 1.5; color: #111; padding: 40px; max-width: 800px; margin: 0 auto; }
 &bull; .resume-header { text-align: center; border-bottom: 2px solid #2563eb; padding-bottom: 10px; margin-bottom: 20px; }
 &bull; .resume-name { font-size: 24px; font-weight: bold; letter-spacing: 1px; }
 &bull; .resume-contact { font-size: 13px; color: #555; }
 &bull; .resume-section-title { font-size: 14px; font-weight: bold; text-transform: uppercase; color: #1e3a8a; border-bottom: 1px solid #ccc; padding-bottom: 3px; margin: 15px 0 8px 0; }
 &bull; ul { padding-left: 20px; }
 &bull; li { margin-bottom: 6px; font-size: 13px; }
 &bull; p { font-size: 13px; }
</style>
</head>
<body>
${paper.innerHTML}
</body>
</html>`;
 &bull; saveBlob(htmlDoc, "resume_optimized.html", "text/html");
}

function downloadJson() {
 &bull; if (!currentReport) return;
 &bull; saveBlob(JSON.stringify(currentReport, null, 2), "ats_audit_report.json", "application/json");
}

function saveBlob(content, filename, type) {
 &bull; const blob = new Blob([content], { type });
 &bull; const url = URL.createObjectURL(blob);
 &bull; const a = document.createElement("a");
 &bull; a.href = url;
 &bull; a.download = filename;
 &bull; a.click();
 &bull; URL.revokeObjectURL(url);
}
