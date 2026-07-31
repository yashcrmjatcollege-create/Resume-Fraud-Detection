import nltk
import re
import PyPDF2
import docx
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')

# ---------------- CONFIG ---------------- #

BUZZWORDS = [
    "expert", "highly skilled", "proficient in all",
    "best", "excellent", "outstanding",
    "world class", "industry leader"
]

SKILLS = [
    "python", "java", "ai", "ml", "blockchain",
    "cloud", "react", "data science"
]

TEMPLATE_TEXT = """
Experienced professional seeking challenging opportunities.
Highly motivated individual with strong communication skills.
"""

COMMON_FAKE_RESUMES = [
    "experienced professional seeking challenging opportunities",
    "highly motivated individual with excellent communication skills",
    "expert in all technologies with proven track record"
]

# ---------------- PREPROCESSING ---------------- #

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    words = text.split()
    words = [w for w in words if w not in stopwords.words('english')]
    return " ".join(words)

# ---------------- NLP HELPERS ---------------- #

def buzzword_score(text):
    return sum(1 for word in BUZZWORDS if word in text)

def similarity_score(text1, text2):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(vectors)[0][1]

def similarity_with_history(new_text, old_texts):
    if not old_texts:
        return 0

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([new_text] + old_texts)
    similarities = cosine_similarity(vectors[0:1], vectors[1:])[0]
    return max(similarities)

# ---------------- MAIN AI LOGIC ---------------- #

def fraud_score(resume_text):
    reasons = []
    score = 0

    clean_text = preprocess(resume_text)
    word_count = len(clean_text.split())

    # 1️⃣ Buzzword detection
    buzz_count = buzzword_score(clean_text)
    if buzz_count > 2:
        score += 25
        reasons.append("Excessive use of generic buzzwords")

    # 2️⃣ Length anomaly
    if word_count < 120:
        score += 20
        reasons.append("Resume is unusually short")
    elif word_count > 1200:
        score += 15
        reasons.append("Resume is unusually long")

    # 3️⃣ Skill overload
    skill_hits = sum(1 for s in SKILLS if s in clean_text)
    if skill_hits > 5:
        score += 25
        reasons.append("Unrealistic number of technical skills listed")

    # 4️⃣ Template similarity
    template_sim = similarity_score(clean_text, TEMPLATE_TEXT)
    if template_sim > 0.45:
        score += 30
        reasons.append("High similarity with common resume templates")

    # 5️⃣ Similarity with fake resume patterns 
    fake_sim = similarity_with_history(clean_text, COMMON_FAKE_RESUMES)
    if fake_sim > 0.60:
        score += 30
        reasons.append("Resume is highly similar to commonly used fake resume templates")

    # 6️⃣ FINALIZE SCORE FIRST
    word_factor = min(len(clean_text.split()) / 300, 1)
    score += word_factor * 10

    # 7️⃣ Verdict
    if score >= 60:
        verdict = "Highly Fraudulent Resume"
    elif score >= 35:
        verdict = "Suspicious Resume"
    else:
        verdict = "Genuine Resume"

    # 8️⃣ Confidence
    if verdict == "Genuine Resume":
        confidence = 90 - score
    elif verdict == "Suspicious Resume":
        confidence = 60 - (score - 35)
    else:
        confidence = 60 + (score - 60)

    confidence = round(min(max(confidence, 30), 95), 2)

    return round(score, 2), verdict, reasons, confidence


# ---------------- FILE TEXT EXTRACTION ---------------- #

def extract_text(file_path, file_type):
    text = ""

    if file_type == "pdf":
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text()

    elif file_type == "docx":
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + " "

    elif file_type == "txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

    return text
