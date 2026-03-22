import streamlit as st
import fitz  # PyMuPDF

st.title("📄 AI Resume Analyzer (Free Version 🚀)")

# -------------------------------
# GLOBAL SKILLS LIST
# -------------------------------
skills_list = [
    "python", "java", "sql", "c++", "javascript",
    "machine learning", "deep learning", "aws",
    "data science", "nlp", "tensorflow", "pytorch",
    "computer vision", "cnn", "reinforcement learning",
    "git", "github", "dbms", "operating systems"
]

# -------------------------------
# FUNCTION: Extract Text
# -------------------------------
def extract_text(file):
    file.seek(0)
    file_bytes = file.read()

    if not file_bytes:
        return ""

    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""

    for page in doc:
        text += page.get_text()

    return text


# -------------------------------
# FUNCTION: Extract Skills
# -------------------------------
def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return found_skills


# -------------------------------
# FUNCTION: ATS SCORE
# -------------------------------
def calculate_ats(resume_skills, job_text):
    job_text = job_text.lower()

    required_skills = [skill for skill in skills_list if skill in job_text]

    matched = []
    missing = []

    for skill in required_skills:
        if skill in resume_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    if len(required_skills) == 0:
        score = 0
    else:
        score = int((len(matched) / len(required_skills)) * 100)

    return score, matched, missing


# -------------------------------
# FUNCTION: FAKE AI SUGGESTIONS 🔥
# -------------------------------
def get_ai_suggestions(skills, missing):
    suggestions = []

    if len(skills) < 5:
        suggestions.append("Add more technical skills to strengthen your resume.")

    if missing:
        suggestions.append(f"Learn these important skills: {', '.join(missing)}")

    if "project" not in skills:
        suggestions.append("Add more real-world projects, especially in AI/ML.")

    suggestions.append("Use strong action words like 'Developed', 'Built', 'Implemented'.")
    suggestions.append("Keep resume concise and ATS-friendly.")
    suggestions.append("Add measurable achievements (e.g., accuracy, performance improvements).")

    return suggestions


# -------------------------------
# JOB DESCRIPTION INPUT
# -------------------------------
st.subheader("📋 Job Description")

jd_option = st.selectbox(
    "Choose a role",
    ["Custom", "AI/ML Intern", "Data Science Intern", "Software Intern"]
)

jd_templates = {
    "AI/ML Intern": "Python, Machine Learning, Deep Learning, Computer Vision, SQL, Git.",
    "Data Science Intern": "Python, SQL, Data Science, Machine Learning, AWS.",
    "Software Intern": "Java/Python, DSA, DBMS, Operating Systems, Git."
}

if jd_option != "Custom":
    job_description = st.text_area("Edit Job Description", jd_templates[jd_option], height=80)
else:
    job_description = st.text_area("Write Job Description", height=80)


# -------------------------------
# FILE UPLOAD
# -------------------------------
uploaded_file = st.file_uploader("📄 Upload your resume (PDF)", type=["pdf"])


# -------------------------------
# MAIN LOGIC
# -------------------------------
if uploaded_file is not None:
    text = extract_text(uploaded_file)

    if text == "":
        st.error("⚠️ Could not read PDF.")
    else:
        st.subheader("📄 Extracted Resume Text")
        st.write(text)

        skills = extract_skills(text)

        st.subheader("🧠 Detected Skills")
        st.success(", ".join(skills))

        if job_description:
            score, matched, missing = calculate_ats(skills, job_description)

            st.subheader("📊 ATS Score")
            st.success(f"{score}% match")

            st.subheader("✅ Matched Skills")
            st.write(", ".join(matched) if matched else "None")

            st.subheader("❌ Missing Skills")
            st.write(", ".join(missing) if missing else "None")

            st.subheader("🚀 Suggested Skills to Learn")
            st.info(", ".join(missing) if missing else "You are job-ready 🎉")

            # FREE AI 🔥
            if st.button("🤖 Get Resume Suggestions"):
                suggestions = get_ai_suggestions(skills, missing)

                st.subheader("💡 Resume Feedback")
                for s in suggestions:
                    st.write(f"- {s}")