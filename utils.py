import PyPDF2
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Extract text from PDF
def extract_text_from_pdf(pdf_file):

    text = ""

    reader = PyPDF2.PdfReader(pdf_file)

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text


# Clean text
def clean_text(text):

    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)

    return text.lower()


# Calculate ATS similarity score
def calculate_similarity(resume, jd):

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([resume, jd])

    similarity = cosine_similarity(vectors)[0][1]

    return round(similarity * 100, 2)


# Extract skills
def extract_skills(text):

    skills_list = [

        "python",
        "java",
        "c",
        "c++",
        "javascript",
        "html",
        "css",

        "machine learning",
        "deep learning",
        "artificial intelligence",
        "nlp",
        "data science",

        "sql",
        "mongodb",
        "mysql",

        "flask",
        "streamlit",
        "react",
        "nodejs",
        "express",

        "tableau",
        "power bi",
        "excel",

        "git",
        "github",
        "api",

        "aws",
        "azure",
        "cloud",

        "tensorflow",
        "pandas",
        "numpy",
        "scikit-learn"
    ]

    found_skills = []

    text = text.lower()

    for skill in skills_list:

        if skill in text:
            found_skills.append(skill)

    return found_skills


# Find missing skills
def missing_skills(resume_skills, jd_skills):

    missing = []

    for skill in jd_skills:

        if skill not in resume_skills:
            missing.append(skill)

    return missing


# Calculate skill match percentage
def calculate_skill_match(resume_skills, jd_skills):

    if len(jd_skills) == 0:
        return 0

    matched = 0

    for skill in jd_skills:

        if skill in resume_skills:
            matched += 1

    return round((matched / len(jd_skills)) * 100, 2)


# AI Resume Feedback Generator
def generate_resume_feedback(score, missing_skills):

    feedback = []

    # Score based feedback
    if score >= 80:

        feedback.append(
            "Your resume is highly optimized for this role."
        )

    elif score >= 60:

        feedback.append(
            "Your resume matches many job requirements but still has room for improvement."
        )

    else:

        feedback.append(
            "Your resume needs significant optimization for this role."
        )

    # Missing skills feedback
    if missing_skills:

        feedback.append(
            "Consider adding the following missing skills:"
        )

        for skill in missing_skills:

            feedback.append(f"• {skill}")

    else:

        feedback.append(
            "Excellent! No major skills are missing."
        )

    # General resume suggestions
    feedback.append(
        "Add more measurable project achievements and impact metrics."
    )

    feedback.append(
        "Use strong action verbs and technical keywords for ATS optimization."
    )

    feedback.append(
        "Include certifications, internships, and relevant technical tools."
    )

    feedback.append(
        "Keep resume formatting clean and ATS-friendly."
    )

    return feedback