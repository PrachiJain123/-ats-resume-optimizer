"""Streamlit Web Application: ATS Resume Optimizer with Antigravity SDK & Gemini 3.1 Pro.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

import streamlit as st

from ats_optimizer.client import AntigravityOptimizerClient
from ats_optimizer.config import (
    DEFAULT_MODEL,
    TARGET_ATS_SCORE,
    get_gemini_api_key,
    save_gemini_api_key,
)
from ats_optimizer.formatter import (
    format_analysis_summary_markdown,
    format_html_resume,
    format_markdown_resume,
    format_xyz_bullet_table_markdown,
)
from ats_optimizer.parser import clean_text, extract_text_from_pdf
from ats_optimizer.samples import SAMPLE_JOB_DESCRIPTIONS, get_default_resume_text

# Page Configuration
st.set_page_config(
    page_title="ATS Resume Optimizer | Gemini 3.1 Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #64748b;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    .badge-x {
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-y {
        background-color: #fef3c7;
        color: #b45309;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-z {
        background-color: #dcfce7;
        color: #15803d;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .kw-chip {
        display: inline-block;
        background: #eef2ff;
        color: #4338ca;
        border: 1px solid #c7d2fe;
        border-radius: 12px;
        padding: 2px 10px;
        font-size: 0.8rem;
        margin: 2px;
        font-weight: 500;
    }
    .bullet-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def init_session_state() -> None:
    if "api_key" not in st.session_state:
        st.session_state.api_key = get_gemini_api_key() or ""
    if "jd_text" not in st.session_state:
        first_title = list(SAMPLE_JOB_DESCRIPTIONS.keys())[0]
        st.session_state.jd_text = SAMPLE_JOB_DESCRIPTIONS[first_title]
    if "resume_text" not in st.session_state:
        st.session_state.resume_text = get_default_resume_text()
    if "report" not in st.session_state:
        st.session_state.report = None


init_session_state()

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.image("https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ff6292a690345.svg", width=42)
    st.title("Antigravity SDK")
    st.caption("Powered by **Gemini 3.1 Pro**")

    st.markdown("---")
    st.subheader("⚙️ Configuration")

    key_input = st.text_input(
        "Gemini API Key",
        value=st.session_state.api_key,
        type="password",
        help="Enter your Gemini API Key. If left empty, high-fidelity offline optimization mode is active.",
    )

    col_save, col_clear = st.columns(2)
    with col_save:
        if st.button("💾 Save Key", use_container_width=True):
            if key_input.strip():
                save_gemini_api_key(key_input.strip())
                st.session_state.api_key = key_input.strip()
                st.success("Saved to .env!")
            else:
                st.warning("Key is empty.")

    model_name = st.selectbox(
        "Model Selection",
        options=["gemini-3.1-pro", "gemini-2.5-pro", "gemini-2.5-flash"],
        index=0,
    )

    target_threshold = st.slider(
        "Target ATS Match Score",
        min_value=85.0,
        max_value=98.0,
        value=TARGET_ATS_SCORE,
        step=1.0,
        format="%d%%",
        help="The optimization loop will iteratively infuse missing JD skills until this match score is reached.",
    )

    st.markdown("---")
    st.subheader("💡 Quick Presets")

    sample_choice = st.selectbox(
        "Load Sample Job Description",
        options=list(SAMPLE_JOB_DESCRIPTIONS.keys()),
        index=0,
    )
    if st.button("📥 Load Preset JD & Resume", use_container_width=True):
        st.session_state.jd_text = SAMPLE_JOB_DESCRIPTIONS[sample_choice]
        st.session_state.resume_text = get_default_resume_text()
        st.session_state.report = None
        st.rerun()

    st.markdown("---")
    if st.session_state.api_key:
        st.success("🟢 API Key Configured (Live Gemini 3.1 Pro Active)")
    else:
        st.info("🟡 Simulation / Heuristic Mode (No API key required to test)")

# ----------------- MAIN VIEW -----------------
st.markdown('<div class="main-header">ATS Resume Optimizer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Extract technical keywords, rewrite bullets using Google\'s <b>XYZ Formula</b>, and guarantee a <b>90%+ ATS Keyword Match</b> with <b>gemini-3.1-pro</b>.</div>',
    unsafe_allow_html=True,
)

# Input Section: 2 Columns
col_jd, col_res = st.columns(2)

with col_jd:
    st.markdown("### 📋 Job Description")
    jd_input = st.text_area(
        "Paste target job description or requirements:",
        value=st.session_state.jd_text,
        height=320,
        key="jd_area",
    )

with col_res:
    st.markdown("### 👤 Resume Input")
    uploaded_pdf = st.file_uploader("Upload Resume PDF (or use text below):", type=["pdf"])

    if uploaded_pdf is not None:
        try:
            pdf_bytes = uploaded_pdf.read()
            extracted_text = extract_text_from_pdf(pdf_bytes)
            st.session_state.resume_text = extracted_text
            st.toast("✅ Extracted text from uploaded PDF!", icon="📄")
        except Exception as e:
            st.error(f"Error parsing PDF: {e}")

    resume_input = st.text_area(
        "Resume Text (Editable):",
        value=st.session_state.resume_text,
        height=240,
        key="resume_area",
    )

# Optimize Button
optimize_btn = st.button("🚀 Optimize Resume for 90%+ ATS Match", type="primary", use_container_width=True)

if optimize_btn:
    if not jd_input.strip() or not resume_input.strip():
        st.error("Please provide both a Job Description and a Resume to optimize.")
    else:
        with st.spinner("Analyzing with Antigravity SDK & Gemini 3.1 Pro..."):
            client = AntigravityOptimizerClient(
                api_key=st.session_state.api_key,
                model=model_name,
            )
            # Run async pipeline
            report = client.optimize_resume_sync(
                jd_text=jd_input,
                resume_text=resume_input,
                target_score=target_threshold,
            )
            st.session_state.report = report
            st.session_state.jd_text = jd_input
            st.session_state.resume_text = resume_input
            st.success("✅ Resume Optimization & 90+ ATS Verification Complete!")

# ----------------- RESULTS VIEW -----------------
if st.session_state.report:
    report = st.session_state.report

    st.markdown("---")
    st.markdown("## 📊 Optimization Results & Scorecard")

    # Metric Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(
            label="Initial ATS Match",
            value=f"{report.initial_score:.1f}%",
            delta=None,
        )
    with m2:
        st.metric(
            label="Post-XYZ Rewriting",
            value=f"{report.post_rewrite_score:.1f}%",
            delta=f"+{report.post_rewrite_score - report.initial_score:.1f}%",
        )
    with m3:
        st.metric(
            label="Final Optimized Score",
            value=f"{report.final_score:.1f}%",
            delta=f"+{report.final_score - report.initial_score:.1f}%",
        )
    with m4:
        status_label = "✅ PASSED (>= 90%)" if report.passed_90 else "⚠️ BELOW TARGET"
        st.metric(
            label="90%+ Threshold Target",
            value=status_label,
        )

    # Visual Progress Bar
    progress_val = min(1.0, report.final_score / 100.0)
    st.progress(progress_val)

    # Tabs for Detailed Breakdown
    tab_bullets, tab_keywords, tab_resume, tab_audit = st.tabs([
        "✍️ Google XYZ Bullets",
        "🏷️ Keyword Matrix & Match",
        "📄 Formatted Resume",
        "⚙️ ATS Audit Trail",
    ])

    # TAB 1: Bullets
    with tab_bullets:
        st.markdown(
            """
            ### Google XYZ Formula Experience Bullets
            > **"Accomplished [X] as measured by [Y], by doing [Z]"**
            - <span class="badge-x">[X] Accomplished</span> : Action verb + core achievement
            - <span class="badge-y">[Y] Measured by</span> : Quantifiable metric, % increase, cost/time saved
            - <span class="badge-z">[Z] By doing</span> : Specific technical tools, architectures, and methodologies
            """,
            unsafe_allow_html=True,
        )

        for i, b in enumerate(report.optimized_bullets, 1):
            with st.container():
                st.markdown(
                    f"""
                    <div class="bullet-card">
                        <div style="font-size:0.85rem; color:#64748b; margin-bottom:4px;"><b>Bullet #{i} — Original:</b></div>
                        <div style="color:#475569; font-style:italic; margin-bottom:8px;">"{b.original}"</div>
                        <div style="font-size:0.9rem; font-weight:600; color:#0f172a; margin-bottom:6px;">✨ Google XYZ Rewritten:</div>
                        <div style="font-size:1rem; color:#1e3a8a; line-height:1.5;">{b.rewritten}</div>
                        <div style="margin-top:8px;">
                            <span class="badge-x">[X]: {b.accomplished_x}</span>
                            <span class="badge-y">[Y]: {b.measured_by_y}</span>
                            <span class="badge-z">[Z]: {b.doing_z}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if b.keywords_infused:
                    chips = "".join(f'<span class="kw-chip">+{k}</span>' for k in b.keywords_infused)
                    st.markdown(f"**Keywords Infused into this bullet:** {chips}", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

    # TAB 2: Keywords
    with tab_keywords:
        st.markdown("### Technical Keyword Match Analysis")

        col_k1, col_k2 = st.columns(2)
        with col_k1:
            st.markdown(f"#### ✅ Matched Keywords ({len(report.post_rewrite_matched)})")
            chips_matched = "".join(f'<span class="kw-chip">{k}</span>' for k in report.post_rewrite_matched)
            st.markdown(chips_matched or "*None*", unsafe_allow_html=True)

        with col_k2:
            st.markdown(f"#### ⚠️ Initial Missing Keywords ({len(report.initial_missing_keywords)})")
            chips_missing = "".join(f'<span class="kw-chip" style="background:#fee2e2; color:#991b1b; border-color:#fca5a5;">{k}</span>' for k in report.initial_missing_keywords)
            st.markdown(chips_missing or "*None! Perfect match.*", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 🗂️ Optimized Technical Competencies Matrix")
        for category, skills in report.optimized_skills_matrix.items():
            if skills:
                st.markdown(f"**{category}:** " + ", ".join(f"`{s}`" for s in skills))

    # TAB 3: Formatted Output
    with tab_resume:
        st.markdown("### Formatted ATS Resume Output")

        md_resume = format_markdown_resume(report, st.session_state.resume_text)
        html_resume = format_html_resume(report, st.session_state.resume_text)

        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            st.download_button(
                label="📥 Download Markdown (.md)",
                data=md_resume,
                file_name="resume_optimized.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with col_d2:
            st.download_button(
                label="🌐 Download Print-Ready HTML (.html)",
                data=html_resume,
                file_name="resume_optimized.html",
                mime="text/html",
                use_container_width=True,
            )
        with col_d3:
            st.download_button(
                label="📊 Download JSON Audit (.json)",
                data=json.dumps(report.to_dict(), indent=2),
                file_name="ats_audit_report.json",
                mime="application/json",
                use_container_width=True,
            )

        resume_view_mode = st.radio("Preview Format:", options=["Rendered Markdown", "Print-Ready HTML", "Raw Markdown"], horizontal=True)

        if resume_view_mode == "Rendered Markdown":
            st.markdown(md_resume)
        elif resume_view_mode == "Print-Ready HTML":
            st.components.v1.html(html_resume, height=900, scrolling=True)
        else:
            st.code(md_resume, language="markdown")

    # TAB 4: Audit
    with tab_audit:
        st.markdown("### ATS 90+ Verification Audit Log")
        for note in report.optimization_notes:
            st.markdown(f"- {note}")

        st.markdown("#### Complete JSON Payload")
        st.json(report.to_dict())
