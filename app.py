import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

from utils import (
    extract_text_from_pdf,
    clean_text,
    calculate_similarity,
    extract_skills,
    missing_skills,
    generate_resume_feedback,
    calculate_skill_match
)

# Page Config
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# Sidebar
st.sidebar.title("🚀 AI Resume Analyzer")

st.sidebar.info("""
Features:
- ATS Score
- Skill Analysis
- Resume Analytics
- AI Suggestions
- Charts & Graphs
""")

# Header
st.markdown("""
<h1 style='text-align:center;'>
🚀 AI Resume Analyzer Dashboard
</h1>
""", unsafe_allow_html=True)

st.write("")

# Upload Section
col1, col2 = st.columns(2)

with col1:
    resume = st.file_uploader(
        "📄 Upload Resume PDF",
        type=["pdf"]
    )

with col2:
    job_description = st.text_area(
        "📝 Paste Job Description"
    )

# Analyze Button
if st.button("Analyze Resume"):

    if resume and job_description:

        # Extract Resume Text
        resume_text = extract_text_from_pdf(resume)

        # Clean Text
        cleaned_resume = clean_text(resume_text)
        cleaned_jd = clean_text(job_description)

        # ATS Score
        score = calculate_similarity(
            cleaned_resume,
            cleaned_jd
        )

        # Skills
        resume_skills = extract_skills(cleaned_resume)
        jd_skills = extract_skills(cleaned_jd)

        missing = missing_skills(
            resume_skills,
            jd_skills
        )

        matched_skills = len(jd_skills) - len(missing)

        skill_match_percent = calculate_skill_match(
            resume_skills,
            jd_skills
        )

        st.write("---")

        # METRICS
        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "ATS Score",
            f"{score}%"
        )

        c2.metric(
            "Matched Skills",
            matched_skills
        )

        c3.metric(
            "Missing Skills",
            len(missing)
        )

        c4.metric(
            "Skill Match %",
            f"{skill_match_percent}%"
        )

        st.progress(int(score))

        # Status
        if score >= 75:
            st.success("Excellent Match 🚀")

        elif score >= 50:
            st.warning("Moderate Match ⚠️")

        else:
            st.error("Low Match ❌")

        st.write("---")

        # SKILLS DISPLAY
        left, right = st.columns(2)

        with left:

            st.subheader("✅ Resume Skills")

            for skill in resume_skills:
                st.markdown(
                    f"""
                    <div style="
                        padding:10px;
                        margin:5px;
                        border-radius:12px;
                        background:#262730;
                        color:white;
                        display:inline-block;
                    ">
                    {skill}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with right:

            st.subheader("❌ Missing Skills")

            if missing:

                for skill in missing:
                    st.markdown(
                        f"""
                        <div style="
                            padding:10px;
                            margin:5px;
                            border-radius:12px;
                            background:#ff4b4b;
                            color:white;
                            display:inline-block;
                        ">
                        {skill}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:
                st.success("No missing skills.")

        st.write("---")

        # CHART SECTION
        st.subheader("📊 Resume Analytics Dashboard")

        chart1, chart2 = st.columns(2)

        # PIE CHART
        with chart1:

            pie_df = pd.DataFrame({
                "Category": [
                    "Matched Skills",
                    "Missing Skills"
                ],
                "Value": [
                    matched_skills,
                    len(missing)
                ]
            })

            fig1 = px.pie(
                pie_df,
                names="Category",
                values="Value",
                title="Skill Distribution"
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

        # BAR CHART
        with chart2:

            bar_df = pd.DataFrame({
                "Metrics": [
                    "ATS Score",
                    "Skill Match"
                ],
                "Values": [
                    score,
                    skill_match_percent
                ]
            })

            fig2 = px.bar(
                bar_df,
                x="Metrics",
                y="Values",
                text="Values",
                title="Resume Performance"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

        st.write("---")

        # RADAR STYLE ANALYTICS
        st.subheader("📈 Resume Strength Analysis")

        analysis_data = pd.DataFrame({
            "Category": [
                "ATS Score",
                "Skill Match",
                "Keyword Optimization",
                "Resume Quality",
                "Technical Alignment"
            ],
            "Score": [
                score,
                skill_match_percent,
                min(score + 10, 100),
                min(score + 5, 100),
                min(skill_match_percent + 8, 100)
            ]
        })

        fig3 = px.line_polar(
            analysis_data,
            r="Score",
            theta="Category",
            line_close=True
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

        st.write("---")

        # AI FEEDBACK
        st.subheader("🤖 AI Resume Feedback")

        feedback = generate_resume_feedback(
            score,
            missing
        )

        for item in feedback:

            st.markdown(
                f"""
                <div style="
                    padding:12px;
                    margin:8px 0;
                    border-radius:12px;
                    background:#1e1e1e;
                    color:white;
                ">
                {item}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("---")

        # Resume Preview
        with st.expander("📄 Resume Preview"):

            st.write(
                resume_text[:4000]
            )

    else:
        st.warning(
            "Please upload resume and enter job description."
        )