# AI Resume Analyzer

An AI-powered tool that analyzes how well a resume matches a given job description. It extracts skills from both documents, compares them using a hybrid of exact keyword matching and semantic similarity (via sentence embeddings), checks the resume's ATS-friendliness, and generates improvement suggestions.

## Features

- Resume upload (PDF) with automatic text extraction
- Match score — percentage alignment between resume and job description
- Existing skills — skills found in both the resume and the job description
- Missing skills — skills required by the job description but not found in the resume
- Semantic matching — catches differently-worded but equivalent skills (e.g. "ML" vs "Machine Learning") using sentence embeddings, not just exact keyword matches
- ATS-friendliness score — flags resume formatting issues (tables, images, low text density) that can confuse Applicant Tracking Systems
- Improvement suggestions — actionable, rule-based feedback based on the match score, missing skills, and ATS issues

## Tech Stack

- Backend framework: FastAPI
- PDF processing: pdfplumber
- Semantic similarity: sentence-transformers (all-MiniLM-L6-v2)
- Frontend: HTML, CSS, JavaScript (served via FastAPI)

## Architecture

Resume (PDF) + Job Description (text)
PDF Text Extraction (pdfplumber)
Text Cleaning (stopword removal)
Skill Extraction (predefined skills list) + ATS-Friendliness Check (tables, images, text density)
Semantic Matching (sentence embeddings, cosine similarity)
Comparison (match score, existing/missing skills)
Suggestions Generator
Results returned to frontend

## Setup

1. Clone the repository

git clone <repo-url>
cd ai-resume-analyzer

2. Create and activate a virtual environment

python -m venv venv
venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Run the server

uvicorn main:app --reload

5. Open the app in your browser

http://localhost:8000/static/index.html

## Known Limitations

- Skill extraction relies on a predefined skills list. Skills not present in this list will not be detected, even by the semantic matching step, since semantic matching only compares skills that were already extracted. This is an intentional scope decision for a beginner-level, time-boxed project — a full solution would require NLP techniques like named entity recognition.
- Semantic matching uses general-purpose sentence embeddings, which are strong at recognizing conceptual synonyms (e.g. "ML" ~ "Machine Learning") but weaker at recognizing that specific named tools serve a similar purpose (e.g. FastAPI and Flask are both Python web frameworks, but their names aren't linguistically similar).
- PDF text extraction works best on single-column, simply-formatted resumes. Complex layouts (multi-column, heavy graphics) may extract text in the wrong order or lose content — this mirrors a real limitation of many ATS parsers.
- Negation and context (e.g. "not experienced in X") are not handled; the system checks for skill presence, not sentiment.

## Project Notes

Detailed concept notes (problem definition, architecture reasoning, NLP concepts, embeddings explanation) are available in the notes/ folder.