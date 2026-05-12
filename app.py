import streamlit as st
from utils import extract_text_from_pdf, clean_text, calculate_similarity

st.set_page_config(page_title="AI Resume Analyzer")

st.title("AI Resume Analyzer & ATS Checker")

resume = st.file_uploader("Upload Resume PDF", type=["pdf"])

job_description = st.text_area("Paste Job Description")

if st.button("Analyze Resume"):

    if resume and job_description:

        resume_text = extract_text_from_pdf(resume)

        cleaned_resume = clean_text(resume_text)
        cleaned_jd = clean_text(job_description)

        score = calculate_similarity(cleaned_resume, cleaned_jd)

        st.subheader(f"ATS Match Score: {score}%")

        if score > 70:
            st.success("Good Match!")
        elif score > 50:
            st.warning("Moderate Match")
        else:
            st.error("Low Match")

        st.subheader("Resume Content")
        st.write(resume_text[:1000])

    else:
        st.warning("Please upload resume and job description.")