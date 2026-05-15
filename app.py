import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from openai import OpenAI
from utils import (
    extract_text_from_pdf,
    clean_text,
    calculate_similarity,
    extract_skills,
    missing_skills,
    generate_resume_feedback,
    calculate_skill_match
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# =========================
# OPENROUTER CONFIG
# =========================

client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)
# =========================
# SESSION STATE
# =========================

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

# =========================
# PDF REPORT FUNCTION
# =========================

def create_pdf_report(score, matched_skills, missing, feedback):

    doc = SimpleDocTemplate("ATS_Report.pdf")

    styles = getSampleStyleSheet()

    content = []

    title = Paragraph(
        "<b>AI Resume Analyzer Report</b>",
        styles['Title']
    )

    content.append(title)

    content.append(Spacer(1, 20))

    ats = Paragraph(
        f"<b>ATS Match Score:</b> {score}%",
        styles['BodyText']
    )

    content.append(ats)

    content.append(Spacer(1, 12))

    matched = Paragraph(
        f"<b>Matched Skills:</b> {matched_skills}",
        styles['BodyText']
    )

    content.append(matched)

    content.append(Spacer(1, 12))

    missing_text = ", ".join(missing)

    missing_para = Paragraph(
        f"<b>Missing Skills:</b> {missing_text}",
        styles['BodyText']
    )

    content.append(missing_para)

    content.append(Spacer(1, 20))

    feedback_title = Paragraph(
        "<b>AI Feedback:</b>",
        styles['Heading2']
    )

    content.append(feedback_title)

    for item in feedback:

        para = Paragraph(
            item,
            styles['BodyText']
        )

        content.append(para)

        content.append(Spacer(1, 8))

    doc.build(content)

    return "ATS_Report.pdf"

# =========================
# GEMINI AI FUNCTION
# =========================
def generate_ai_feedback(resume_text, job_description):

    prompt = f"""
    Analyze this resume against the given job description.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Provide:
    1. ATS Match Score (out of 100)
    2. Missing Skills
    3. Resume Strengths
    4. Suggested Improvements
    5. Final Recommendation
    """

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

# =========================
# AI RESUME REWRITER
# =========================

def rewrite_resume_text(text, mode):

    prompt = f"""

    Rewrite this resume bullet point professionally.

    Rewrite Style:
    {mode}

    Requirements:
    - ATS optimized
    - professional tone
    - impactful wording
    - concise
    - technical language
    - strong action verbs

    Resume Content:
    {text}

    """

    response = client.chat.completions.create(

        model="deepseek/deepseek-chat",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]

    )

    return response.choices[0].message.content


# =========================
# SIDEBAR
# =========================

st.sidebar.title("🚀 AI Resume Analyzzer")

st.sidebar.info("""
Features:
- ATS Score
- Skill Analysis
- Resume Analytics
- Gemini AI Suggestions
- PDF Report
- Interactive Charts
""")

# =========================
# HEADER
# =========================

st.markdown("""
<h1 style='text-align:center;'>
🚀 AI Resume Analyzer Dashboard
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
padding:20px;
border-radius:15px;
background: linear-gradient(to right, #141e30, #243b55);
color:white;
text-align:center;
margin-bottom:20px;
">
<h3>AI-Powered ATS Resume Screening System</h3>
<p>NLP • Machine Learning • Gemini AI • Analytics Dashboard</p>
</div>
""", unsafe_allow_html=True)

# =========================
# INPUT SECTION
# =========================

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

# =========================
# ANALYZE BUTTON
# =========================

analyze_clicked = st.button("Analyze Resume")

if analyze_clicked:

    if resume and job_description:

        # Extract Text
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

        # Missing Skills
        missing = missing_skills(
            resume_skills,
            jd_skills
        )

        matched_skills = len(jd_skills) - len(missing)

        skill_match_percent = calculate_skill_match(
            resume_skills,
            jd_skills
        )

        # Feedback
        feedback = generate_resume_feedback(
            score,
            missing
        )

        # Save State
        st.session_state.analysis_done = True
        st.session_state.resume_text = resume_text
        st.session_state.job_description = job_description
        st.session_state.score = score
        st.session_state.resume_skills = resume_skills
        st.session_state.jd_skills = jd_skills
        st.session_state.missing = missing
        st.session_state.feedback = feedback
        st.session_state.matched_skills = matched_skills
        st.session_state.skill_match_percent = skill_match_percent

# =========================
# DISPLAY RESULTS
# =========================

if st.session_state.analysis_done:

    score = st.session_state.score
    resume_skills = st.session_state.resume_skills
    jd_skills = st.session_state.jd_skills
    missing = st.session_state.missing
    feedback = st.session_state.feedback
    matched_skills = st.session_state.matched_skills
    skill_match_percent = st.session_state.skill_match_percent
    resume_text = st.session_state.resume_text

    st.write("---")

    # Metrics
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

    # Skills Display
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

    # Analytics
    st.subheader("📊 Resume Analytics Dashboard")

    chart1, chart2 = st.columns(2)

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

    # Radar Chart
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

    # AI Feedback
    st.subheader("🤖 AI Resume Feedback")

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

    # PDF Report
    st.subheader("📥 Download ATS Report")

    pdf_file = create_pdf_report(
        score,
        matched_skills,
        missing,
        feedback
    )

    with open(pdf_file, "rb") as file:

        st.download_button(
            label="Download PDF Report",
            data=file,
            file_name="ATS_Report.pdf",
            mime="application/pdf"
        )

    st.write("---")

    # OpenRouter AI Review
    st.subheader("🧠 OpenRouter AI Resume Review")

    if st.button("Generate AI Suggestions"):

        with st.spinner(
            "🤖 OpenRouter AI is analyzing your resume..."
        ):

            ai_feedback = generate_ai_feedback(
                st.session_state.resume_text,
                st.session_state.job_description
            )

            st.markdown(
                f"""
                <div style="
                    padding:20px;
                    border-radius:15px;
                    background:#111827;
                    color:white;
                    line-height:1.8;
                    font-size:16px;
                ">
                {ai_feedback}
                </div>
                """,
                unsafe_allow_html=True
            )
        st.write("---")

    # =========================
    # AI RESUME REWRITER
    # =========================

    st.subheader("✍ AI Resume Rewriter")

    st.markdown("""
    Improve resume bullet points using AI-powered ATS optimization.
    """)

    rewrite_mode = st.selectbox(

        "Choose Rewrite Style",

        [
            "Professional",
            "ATS Optimized",
            "Technical",
            "Concise"
        ]
    )

    rewrite_text = st.text_area(
        "Enter Resume Bullet Point",
        height=150,
        placeholder="Example: Built chatbot using Python"
    )

    if st.button("Rewrite Resume Content"):

        if rewrite_text:

            with st.spinner(
                "🤖 AI is rewriting your content..."
            ):

                rewritten = rewrite_resume_text(
                    rewrite_text,
                    rewrite_mode
                )

                st.success(
                    "AI-Rewritten Resume Content"
                )

                st.markdown(
                    f"""
                    <div style="
                        padding:25px;
                        border-radius:15px;
                        background: linear-gradient(to right, #141e30, #243b55);
                        color:white;
                        line-height:1.8;
                        font-size:17px;
                        margin-top:10px;
                    ">
                    {rewritten}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.warning(
                "Please enter resume content."
            )

            
    st.write("---")

    # Resume Preview
    with st.expander("📄 Resume Preview"):

        st.write(
            resume_text[:4000]
        )

# =========================
# FOOTER
# =========================

st.write("---")

st.markdown("""
<center>
Built with ❤️ using Python, Streamlit, NLP, Plotly & Gemini AI
</center>
""", unsafe_allow_html=True)