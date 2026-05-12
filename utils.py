import PyPDF2
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)

    for page in reader.pages:
        text += page.extract_text()

    return text

# Clean text
def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    return text.lower()

# Calculate ATS score
def calculate_similarity(resume, jd):
    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([resume, jd])

    similarity = cosine_similarity(vectors)[0][1]

    return round(similarity * 100, 2)