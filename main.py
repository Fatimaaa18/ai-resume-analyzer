from fastapi import FastAPI, UploadFile, Form
import pdfplumber
from preprocessing.clean_text import clean_text
from skills_extraction.extract_skills import extract_skills
from comparison.compare_skills import compare_skills
from semantic_matching.semantic_match import get_semantic_matches
from ats_check.ats_score import check_ats_friendliness
from suggestions.generate_suggestions import generate_suggestions
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="AI Resume Analyzer")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return {"status": "AI Resume Analyzer API is running"}
@app.post("/analyze")
def analyze(resume: UploadFile, job_description: str = Form(...)):
    with pdfplumber.open(resume.file) as pdf:
        resume_text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                resume_text += page_text + "\n"

    resume.file.seek(0)
    ats_result = check_ats_friendliness(resume.file)

    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description)

    resume_skills = extract_skills(cleaned_resume)
    jd_skills = extract_skills(cleaned_jd)

    semantic_matches = get_semantic_matches(resume_skills, jd_skills)
    resume_skills_expanded = resume_skills | semantic_matches

    result = compare_skills(resume_skills_expanded, jd_skills)
    result = compare_skills(resume_skills_expanded, jd_skills)

    suggestions = generate_suggestions(
        match_score=result["match_score"],
        missing_skills=result["missing_skills"],
        ats_issues=ats_result["issues"]
    )

        
    return {
        "resume_filename": resume.filename,
        "match_score": result["match_score"],
        "existing_skills": result["existing_skills"],
        "missing_skills": result["missing_skills"],
        "ats_score": ats_result["ats_score"],
        "ats_issues": ats_result["issues"],
        "suggestions": suggestions
    }