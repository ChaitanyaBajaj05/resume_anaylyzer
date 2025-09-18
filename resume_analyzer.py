import re
import docx
import PyPDF2

# -------------------------------
# Resume Text Extractors
# -------------------------------
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text


def extract_text_from_docx(file_path):
    text = ""
    doc = docx.Document(file_path)
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text


def clean_text(text):
    return re.sub(r"\s+", " ", text).lower()


# -------------------------------
# Resume Analyzer
# -------------------------------
def analyze_resume(resume_text, job_description):
    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    # Extract keywords from job description
    job_keywords = set(re.findall(r"\b[a-zA-Z]{3,}\b", job_description))

    found_skills = [word for word in job_keywords if word in resume_text]
    missing_skills = [word for word in job_keywords if word not in resume_text]

    score = int((len(found_skills) / len(job_keywords)) * 100) if job_keywords else 0

    return score, found_skills, missing_skills


# -------------------------------
# Main Function
# -------------------------------
if __name__ == "__main__":
    print("=== AI Resume Analyzer ===")

    file_path = input("Enter resume file path (PDF/DOCX): ")
    if file_path.endswith(".pdf"):
        resume_text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        resume_text = extract_text_from_docx(file_path)
    else:
        print("❌ Unsupported file format. Use PDF or DOCX.")
        exit()

    job_description = input("\nPaste Job Description: ")

    score, found, missing = analyze_resume(resume_text, job_description)

    print("\n✅ Match Score:", score, "%")
    print("🔑 Skills Found:", ", ".join(found) if found else "None")
    print("❌ Missing Skills:", ", ".join(missing) if missing else "None")
