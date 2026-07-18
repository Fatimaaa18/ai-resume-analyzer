# AI Resume Analyzer — Complete Project Notes

**Part 1** covers the problem, requirements, architecture, and technology decisions (planning phase).
**Part 2** covers the actual implementation (FastAPI, PDF processing, NLP pipeline, embeddings, ATS check, frontend).

---

# Part 1: Problem, Requirements, Architecture & Tech Stack

**Project:** AI Resume Analyzer
**Covers:** Step 1 (Understand the Problem) → Step 4 (Compare & Choose Technologies)

---

## 1. What Is It?

The AI Resume Analyzer is a system where a user uploads their resume (PDF) and pastes a job description (JD). The system analyzes both and returns:

- Match Score (%)
- Existing Skills (skills present in both resume and JD)
- Missing Skills (skills in JD but not in resume)
- ATS-Friendliness Score
- Improvement Suggestions

---

## 2. Why Do We Need It?

Resumes are commonly screened by **Applicant Tracking Systems (ATS)** before a human ever sees them. Qualified candidates get rejected for two independent reasons:

1. **Poor formatting** — the resume's structure (tables, columns, graphics, unusual fonts) prevents the ATS parser from correctly reading the text.
2. **Keyword/content mismatch** — the resume doesn't contain the same words as the job description, even if the candidate has the relevant skills, because they phrased things differently (e.g. "ML" vs "Machine Learning").

This project addresses both problems.

---

## 3. What Problem Does It Solve?

It gives job-seekers visibility into:
- How well their resume aligns with a specific job description (content-level)
- Whether their resume's format is machine-readable at all (structure-level)
- What specific skills are missing
- How to improve the resume for both machines (ATS) and humans (recruiters)

---

## 4. Two Types of "Score" — A Critical Distinction

| | Match Score | ATS-Friendliness Score |
|---|---|---|
| Depends on | Job description content | Resume's format/structure |
| Changes with | Every new job description | Stays the same regardless of JD |
| Answers | "Am I qualified for this job?" | "Can a machine even read my resume?" |

```
Resume (PDF)
    │
    ├──► Structure/Format Check ──► ATS-Friendliness Score
    │      (tables? columns? images? fonts?)
    │
    └──► Content Extraction (text)
              │
              └──► Compare with Job Description ──► Match Score
                                                      + Missing Skills
                                                      + Existing Skills
```

---

## 5. Requirements

### Functional Requirements

| # | Requirement |
|---|---|
| FR1 | User can upload resume in PDF format |
| FR2 | User can paste job description text |
| FR3 | System extracts raw text from the PDF |
| FR4 | System calculates a Match Score (%) |
| FR5 | System lists Existing Skills (matched between resume & JD) |
| FR6 | System lists Missing Skills (in JD, not in resume) |
| FR7 | System gives resume improvement suggestions |
| FR8 | System gives an ATS-Friendliness Score (format-based, independent of JD) |

### Non-Functional Requirements

| # | Requirement |
|---|---|
| NFR1 | Entire system built with free tools/libraries only |
| NFR2 | Realistically completable in ~2 weeks |
| NFR3 | Clean, modular, professional (GitHub-worthy) code |
| NFR4 | System supports reasonably-formatted resumes; complex graphic-heavy resumes are best-effort only |
| NFR5 | Skill extraction uses a hybrid approach: predefined skills list + AI/NLP semantic matching (to avoid the Out-of-Vocabulary problem) |
| NFR6 | System uses basic semantic similarity to reduce exact-keyword-matching limitations (e.g. "ML" vs "Machine Learning"). Full negation-handling / deep-context-understanding is out of scope for this beginner-level, 2-week project. |

---

## 6. Key NLP Concepts Discovered While Defining Requirements

### 6.1 Keyword Matching vs Semantic Matching

- **Exact/Keyword Matching:** Simple string comparison (e.g. "Python" in resume = "Python" in JD). Fast, simple, but rigid.
- **Semantic Matching:** Understanding that two differently-worded phrases mean the same thing (e.g. "Machine Learning" vs "TensorFlow-based deep learning models"). Requires actual meaning-based understanding, not just string comparison.

**Why simple keyword matching alone is unreliable:** A genuinely qualified candidate can be rejected simply because they didn't use the exact words the JD used — the system can't understand the relationship between the words, it just looks for exact matches.

### 6.2 Stopwords Removal

Common filler words ("the", "is", "a", "and", "with", "using") that appear frequently but carry no meaningful information. Removing them isolates the content-rich words. This is a simple, rule-based operation — matching against a predefined list, no AI involved.

### 6.3 Skill Extraction — Two Approaches

- **Approach A (Predefined Skills Dictionary):** A fixed list of known skill names (e.g. `["python", "sql", "aws", ...]`). Simple and fast, but suffers from the **Out-of-Vocabulary (OOV) Problem** — any skill not already in the list will never be detected (new technologies, spelling variations, abbreviations, niche skills).
- **Approach B (AI/NLP-based Extraction):** A model infers from context which words are skills, even if they weren't in a predefined list. More flexible, but more complex.

**Decision:** Use a **Hybrid Approach** — predefined list for fast/reliable baseline coverage, AI/semantic understanding to catch what the list misses.

### 6.4 N-grams (Multi-word Phrases)

Some skills are single words ("Django"), but many are multi-word phrases ("data structures", "REST API design"). If a system only looks at individual words, it loses the combined meaning. Considering word combinations (bigrams, trigrams) instead of just single words (unigrams) preserves this meaning.

### 6.5 Negation Handling (Context)

A sentence like *"Not experienced in machine learning"* contains the keyword "machine learning" but means the opposite of having that skill. Simple keyword presence checks cannot detect this — it requires understanding the relationship between words in a sentence, not just their presence.

**Scope decision:** Full negation/context handling is a hard, research-level NLP problem. Given the 2-week, beginner-level scope of this project, we are **not** attempting full negation handling — we're using "good enough" semantic similarity instead. This is a deliberate, documented trade-off ("perfect is the enemy of good"), not a shortcut taken by accident.

### 6.6 One Core Comparison Logic Drives Three Features

Match Score, Existing Skills, and Missing Skills all come from the same underlying operation: comparing a resume's skill list against a JD's skill list.

```
Core Comparison Logic
         │
         ├──► Resume Skills ∩ JD Skills = Existing Skills
         │
         ├──► JD Skills − Resume Skills = Missing Skills
         │
         └──► (Existing Skills / Total JD Skills) × 100 = Match Score (%)
```

This reflects the **DRY (Don't Repeat Yourself)** principle — one core logic, reused across multiple features, instead of separate logic per feature.

---

## 7. Architecture

### 7.1 User Flow

```
User
  │
  ├──► Resume Upload (PDF)
  │
  ├──► Job Description Paste (Text)
  │
  ├──► Click "Analyze" Button
  │
  ▼
[System Processing...]
  │
  ▼
Final Result Displayed:
  ├── Match Score
  ├── Existing Skills
  ├── Missing Skills
  ├── ATS-Friendliness Score
  └── Improvement Suggestions
```

### 7.2 Backend Processing Pipeline (Behind the "Analyze" Click)

```
Step 1: Resume PDF → raw text extraction
Step 2: Raw text cleaning (stopwords removal, formatting cleanup)
Step 3: Skill extraction from resume (hybrid: list + semantic AI)
Step 4: Skill extraction from JD (same process)
Step 5: Compare both skill lists (core comparison logic)
Step 6: Calculate Match Score, Existing Skills, Missing Skills
Step 7: ATS-Friendliness check (structure/format — independent of JD)
Step 8: Generate improvement suggestions
Step 9: Combine all results → send back to user
```

### 7.3 Frontend vs Backend

- **Frontend** = what the user sees/interacts with (upload button, textbox, results)
- **Backend** = where the actual processing/logic happens (PDF extraction, NLP, scoring)

**Decision:** The project is backend/AI-heavy by design (~80–85% effort), since the core learning goal is AI Engineering, not frontend design. The frontend will be simple but presentable (not "fancy") — important since a demo video will be shared on LinkedIn, so first impressions still matter, just without heavy time investment.

### 7.4 Sequential vs Parallel Steps

Not all 9 pipeline steps strictly depend on each other:

| Step | Depends on | Sequential or Parallel? |
|---|---|---|
| PDF Text Extraction | Nothing | Must be first |
| Skill Extraction (Resume) | PDF text extraction | Sequential |
| Skill Extraction (JD) | Nothing (JD is already text) | Parallel with resume processing |
| ATS-Friendliness Check | PDF structure | Parallel with skill extraction |
| Comparison | Both skill lists | Waits for both to finish |
| Suggestions | Comparison result | Sequential, after comparison |

**Scope decision:** True parallel programming (async/threading) is a complex topic on its own and adds implementation overhead disproportionate to the benefit at this scale. The architecture is designed to be conceptually modular (so it *could* be parallelized later), but the initial implementation will run sequentially for simplicity.

### 7.5 Communication Between Frontend and Backend

- **HTTP (HyperText Transfer Protocol):** A standardized set of rules for how two programs exchange data over the internet — a request goes out, a response comes back.
- **Request** contains: Method (GET/POST/PUT/DELETE), URL/Endpoint, Body (data being sent).
- **Response** contains: Status Code (200 = success, 404 = not found, 500 = server error), Body (data returned).
- **API (Application Programming Interface):** A contract defining what endpoints exist, what to send, and what you'll get back — like a restaurant menu.
- **REST:** A style/convention for designing APIs (clear resource URLs, consistent use of HTTP methods, statelessness). "REST API" = an API that follows REST conventions.
- **Flask/FastAPI:** Not "types of API" — they are Python *tools/frameworks* used to build REST APIs.

**Our app's endpoint:** `POST /analyze` — POST is used because the frontend is *submitting* data (resume file + JD text) to the server for processing, not just requesting existing data (which would be GET).

---

## 8. Technology Stack — Final Decisions

| Component | Choice | Why |
|---|---|---|
| Backend Framework | **FastAPI** | Built specifically for APIs; has automatic request validation (via Pydantic + type hints) and automatic interactive API documentation (Swagger UI). Saves time versus Flask, where these are manual — important given the 2-week timeline and the amount of new NLP/AI content already being learned. |
| PDF Processing | **pdfplumber** | Simple to use, and handles typical resume formatting (bullet points, spacing) better than the more minimal `pypdf`, which matters since almost all real resumes have some formatting. |
| Skill Matching Approach | **Hybrid** (predefined skills list + embeddings) | Predefined list gives fast, reliable coverage of common skills; embeddings catch synonyms/variations the list misses (solves the OOV problem). |
| Semantic Similarity | **Local, lightweight embedding model** | Free (no paid API), works offline, and fits within an 8GB RAM constraint — unlike large generative chatbot models, embedding models only need to output a single vector per input (no multi-step text generation), so they can be far smaller and lighter. |
| Frontend | **Streamlit** | Pure Python — no need to learn HTML/CSS/JavaScript or a JS framework. Keeps focus on AI/backend learning within the 2-week timeline, while still producing a clean, professional, demo-ready interface (also a common choice for real-world AI/ML portfolio projects). |

---

## 9. Embeddings — Core AI Concept

### What Is It?

A way of converting text (a word, phrase, or sentence) into a **vector** — a list of many numbers (not just one) — such that texts with similar meaning end up numerically close together in that multi-dimensional space.

### Why Not Just Assign Each Word a Single Number?

Assigning arbitrary numbers (King=1, Queen=2, Apple=3) encodes no meaning — the numeric distance between 1 and 2 is the same as between 1 and 3, even though "King" and "Queen" are conceptually much closer than "King" and "Apple." A single number/dimension isn't enough to represent meaning — multiple numbers (dimensions) are needed, where each dimension can capture a different aspect of meaning.

### How It Works (Simplified Example)

```
King  = [0.9, 0.8, 0.1]
Queen = [0.9, 0.2, 0.1]
Apple = [0.0, 0.0, 0.9]
```

King and Queen are numerically close (similar meaning); King and Apple are far apart. Real embeddings use hundreds of dimensions, and the individual dimensions aren't human-labeled like this — the model learns them during training.

### How It's Used in This Project

To catch cases where the resume and JD use different words for the same skill (e.g. "ML" vs "Machine Learning"), we convert both into embeddings and measure how close their vectors are (a **similarity score**, 0 to 1). This is calculated using a method called **cosine similarity** (covered in detail during implementation).

### Pre-trained Models

We won't train our own embedding model (requires huge datasets/compute). Instead we use a **pre-trained model** — already trained by someone else — purely for **inference** (using it to generate embeddings for our text).

### Local vs API-based Models

| | API-based (e.g. OpenAI) | Local Model |
|---|---|---|
| Cost | Usually paid | Free |
| Internet required | Yes | No (after download) |
| Uses your hardware | No | Yes (RAM/CPU) |

**Decision:** Local model — required by NFR1 (everything free). Concern about RAM (8GB laptop) is addressed by choosing a **lightweight** embedding model (not a full generative chatbot model) — embedding models only need to output one vector per input in a single pass, unlike chatbot models which generate text token-by-token, so they require far fewer resources. Specific model name to be finalized during implementation.

---

## 10. Decisions Log

- Backend Framework: **FastAPI**
- PDF Processing Library: **pdfplumber**
- Skill Matching: **Hybrid** (predefined list + embeddings)
- Embedding Model: **Local, lightweight** (specific model TBD during implementation)
- Frontend: **Streamlit**
- Parallel processing: Designed for conceptually, implemented sequentially (v1)
- Negation/deep context handling: Out of scope for this project
- Frontend effort: Minimal but presentable (not fancy) — LinkedIn demo consideration


---


# Part 2: Implementation — FastAPI, PDF Processing, NLP Pipeline, Embeddings, ATS Check, Frontend

**Project:** AI Resume Analyzer
**Covers:** Step 5 (Learn Concepts) → Step 9 (Build Frontend)

---

## 1. FastAPI Basics

### ASGI and Uvicorn

A normal Python script runs once and exits. An API server needs to run continuously, listening for incoming requests. This requires:

- **ASGI (Asynchronous Server Gateway Interface):** a standard/protocol defining how a Python web application and a server communicate, and how it can handle multiple requests concurrently (asynchronously) without blocking.
- **Uvicorn:** the actual software that implements the ASGI standard — it listens for incoming HTTP requests, hands them to the FastAPI application, and sends the response back.

```
[Browser/Frontend] → [Uvicorn: listens for requests] → [FastAPI app: decides response] → [Uvicorn sends it back]
```

### Routes and Decorators

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "..."}
```

- `FastAPI()` creates the application object.
- `@app.get("/")` is a decorator that registers a function as an event handler — when a GET request hits `/`, FastAPI automatically calls `read_root()`. This is a callback/event-driven pattern, not a manual function call.
- Returning a Python dictionary is automatically converted by FastAPI into JSON, since JSON (not a language-specific Python dictionary) is the universal, text-based format that any frontend, in any language, can understand.

### Pydantic and Data Validation

FastAPI uses Pydantic models (`BaseModel`) combined with Python type hints to automatically validate incoming request data, without writing manual `if/else` checks. This — along with automatic interactive documentation at `/docs` (Swagger UI) — was the main reason FastAPI was chosen over Flask for this project: it saves time on boilerplate so more time can go toward the actual NLP/AI logic.

### File Uploads

A file (like a PDF) is binary data, not text, so it can't be represented as a plain string in a Pydantic model. FastAPI instead uses `UploadFile` as a parameter type, and when a file and text are sent together, the request format is `multipart/form-data` (not JSON) — text fields are marked with `Form(...)`.

```python
from fastapi import UploadFile, Form

@app.post("/analyze")
def analyze(resume: UploadFile, job_description: str = Form(...)):
    ...
```

---

## 2. PDF Text Extraction (pdfplumber)

A PDF stores text as characters with individual (x, y) coordinates for rendering — it has no inherent concept of "words" or "reading order." A PDF extraction library must:

1. Read all characters and their coordinates.
2. Group nearby characters into words, based on proximity.
3. Group words into lines, based on shared y-coordinates.
4. Guess a reading order for lines/blocks — this is the hardest part and is done through heuristics, not true understanding.

This is why simple, single-column resumes extract cleanly, while multi-column/table layouts can scramble the extracted text order — this directly informed the project's accepted scope limitation (NFR4: complex layouts are best-effort only).

```python
import pdfplumber

with pdfplumber.open(resume.file) as pdf:
    resume_text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            resume_text += page_text + "\n"
```

Note: when the same `UploadFile.file` stream needs to be read a second time (e.g. once for text extraction, once for the ATS structural check), the stream's read cursor must be rewound first with `resume.file.seek(0)`, otherwise the second read returns nothing — the stream has already been fully consumed.

---

## 3. Text Cleaning (Stopwords)

Common filler words ("the", "is", "and", etc.) are removed using a predefined set, and text is lowercased so that "Python" and "python" are treated identically. This is a fast, purely rule-based step — no AI involved.

```python
STOPWORDS = {"a", "an", "the", ...}

def clean_text(text: str) -> str:
    text = text.lower()
    words = text.split()
    cleaned_words = [word for word in words if word not in STOPWORDS]
    return " ".join(cleaned_words)
```

A `set` (not a `list`) is used for the stopwords collection because membership checks (`word not in STOPWORDS`) are much faster on a set.

---

## 4. Skill Extraction (Predefined List)

```python
SKILLS_LIST = {"python", "sql", "fastapi", "data structures", ...}

def extract_skills(cleaned_text: str) -> set:
    found_skills = set()
    for skill in SKILLS_LIST:
        if skill in cleaned_text:
            found_skills.add(skill)
    return found_skills
```

Checking `if skill in cleaned_text` performs a substring search, which also naturally catches multi-word skills (like "data structures") as long as the words appear consecutively in the source text.

**Known limitation:** this extraction step only ever detects skills that exist in `SKILLS_LIST`. A skill mentioned in the resume using completely different wording, or a skill not in the list at all (e.g. a newer tool), will never be extracted — regardless of how good the later semantic matching step is. Semantic matching only compares *already-extracted* skills against each other; it cannot rescue a skill that extraction missed entirely. Fully solving this would require NLP techniques such as named entity recognition, which is out of scope for this project. This was a deliberate, documented trade-off, not an oversight.

---

## 5. Semantic Matching (Embeddings)

### Why Needed

Exact keyword matching fails when the resume and job description use different wording for the same skill (e.g. "ML" vs "Machine Learning"). Embeddings solve this by converting text into vectors (lists of numbers) such that similar-meaning text ends up numerically close together.

### Implementation

```python
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_semantic_matches(resume_skills: set, jd_skills: set, threshold: float = 0.6) -> set:
    additional_matches = set()
    jd_missing = jd_skills - resume_skills

    for jd_skill in jd_missing:
        jd_embedding = model.encode(jd_skill, convert_to_tensor=True)
        for resume_skill in resume_skills:
            resume_embedding = model.encode(resume_skill, convert_to_tensor=True)
            similarity = util.cos_sim(jd_embedding, resume_embedding).item()
            if similarity >= threshold:
                additional_matches.add(jd_skill)
                break

    return additional_matches
```

- `all-MiniLM-L6-v2` is a small, local, pre-trained embedding model (~90MB) — free, works offline once downloaded, and light enough to run on 8GB RAM, unlike large generative language models. It only outputs one vector per input in a single pass (no multi-step text generation), which is why it can be so much smaller.
- `util.cos_sim(...)` computes **cosine similarity** — a number between 0 and 1 indicating how close two vectors are in meaning.
- Only `jd_missing` (skills in the JD not already exact-matched) are checked, to avoid unnecessary computation.
- `break` stops the inner loop as soon as one sufficiently similar resume skill is found — the goal here is only a yes/no answer per JD skill ("is there *some* equivalent in the resume?"), not identifying the single best match, so continuing to check the rest is unnecessary once a match is confirmed.

### Threshold Trade-off

Lowering the similarity threshold increases recall (catches more genuine matches, e.g. "FastAPI" vs "Flask") but also increases false positives (unrelated skills incorrectly marked as matching). `0.6` was kept as a deliberate, documented choice, favoring precision over recall — an incorrect "you have this skill" match is more misleading to a user than a missed one.

**Observed limitation:** the model recognizes conceptual synonyms well (e.g. "ML" ≈ "Machine Learning") but is weaker at recognizing that two differently-named tools serve a similar purpose (e.g. "FastAPI" and "Flask" are both Python web frameworks, but the words themselves aren't linguistically similar). This is a general-purpose embedding model, not one fine-tuned on technical/domain-specific relationships.

---

## 6. Comparison Logic

```python
def compare_skills(resume_skills: set, jd_skills: set) -> dict:
    existing_skills = resume_skills & jd_skills
    missing_skills = jd_skills - resume_skills

    if len(jd_skills) == 0:
        match_score = 0
    else:
        match_score = round((len(existing_skills) / len(jd_skills)) * 100, 2)

    return {
        "match_score": match_score,
        "existing_skills": list(existing_skills),
        "missing_skills": list(missing_skills)
    }
```

- `&` (set intersection) gives existing skills; `-` (set difference) gives missing skills.
- A single core comparison function derives all three related outputs (match score, existing skills, missing skills) — following the DRY principle established during the design phase.
- Sets must be converted to `list(...)` before returning in an API response, since JSON has no native representation for a Python `set`.

Before this comparison runs, the resume's exact-matched skills are expanded with any semantic matches found:
```python
resume_skills_expanded = resume_skills | semantic_matches
```
(`|` is set union.)

---

## 7. ATS-Friendliness Check

This check is independent of the job description — it only examines the resume's structure.

```python
def check_ats_friendliness(pdf_file) -> dict:
    score = 100
    issues = []

    with pdfplumber.open(pdf_file) as pdf:
        total_tables = 0
        total_images = 0
        total_text_length = 0

        for page in pdf.pages:
            total_tables += len(page.find_tables())
            total_images += len(page.images)
            page_text = page.extract_text()
            if page_text:
                total_text_length += len(page_text)

        if total_tables > 0:
            score -= 20
            issues.append("...")
        if total_images > 0:
            score -= 15
            issues.append("...")
        if total_text_length < 200:
            score -= 25
            issues.append("...")

    return {"ats_score": max(score, 0), "issues": issues}
```

- `page.find_tables()` and `page.images` are pdfplumber's built-in structural detectors.
- A low extracted-text length is used as a heuristic signal for heavily graphic/complex formatting — if this tool's own extractor struggles, a real-world ATS parser likely would too.
- `max(score, 0)` prevents the score from going negative if multiple issues stack up.

---

## 8. Suggestions Generator

A deliberately rule-based (not AI-based) module — no new model is needed here, since the inputs (match score, missing skills, ATS issues) are already structured data from earlier steps.

```python
def generate_suggestions(match_score, missing_skills, ats_issues) -> list:
    suggestions = []
    if match_score < 50:
        suggestions.append("...")
    elif match_score < 75:
        suggestions.append("...")
    else:
        suggestions.append("...")

    if missing_skills:
        suggestions.append(f"Consider adding: {', '.join(missing_skills)}.")

    if ats_issues:
        for issue in ats_issues:
            suggestions.append(f"- {issue}")
    else:
        suggestions.append("Your resume format appears ATS-friendly.")

    return suggestions
```

---

## 9. Full Pipeline (main.py)

```
POST /analyze receives resume (UploadFile) + job_description (Form)
  → extract text from all PDF pages (pdfplumber)
  → seek(0), run ATS-friendliness check on the same file stream
  → clean_text() on resume text and job description
  → extract_skills() on both (predefined list)
  → get_semantic_matches() to catch differently-worded equivalents
  → expand resume skills with semantic matches (set union)
  → compare_skills() → match score, existing skills, missing skills
  → generate_suggestions() using match score, missing skills, ATS issues
  → return combined JSON response
```

---

## 10. Frontend

### Why Streamlit Was Dropped

Streamlit was the original planned choice (pure Python, no HTML/CSS/JS needed). During implementation, a persistent local environment issue prevented the Streamlit dev server's background requests from reaching the browser (confirmed via terminal-level requests succeeding while browser requests failed, across multiple browsers and incognito mode) — the root cause was not resolved within a reasonable time.

### Practical Alternative: FastAPI Serving Static HTML

Instead, the backend itself serves a single static HTML/CSS/JS page, using FastAPI's `StaticFiles`:

```python
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
```

The page (`static/index.html`) contains:
- A file upload input and a textarea, styled with plain CSS (dark theme, card-based layout, color-coded progress bars and skill tags).
- JavaScript that, on button click, packages the file and text into a `FormData` object and sends it via `fetch()` as a POST request to `/analyze` — the same endpoint already built and tested via `/docs`.
- The JSON response is used to dynamically update the score bars, skill tag lists, and suggestions text in the page.

Because the frontend is served from the same FastAPI server (`localhost:8000`), the browser-facing part of the app runs on a URL that was already confirmed working, avoiding the need for a second server/port.

```javascript
const formData = new FormData();
formData.append('resume', resumeFile);
formData.append('job_description', jobDescription);

const response = await fetch('/analyze', { method: 'POST', body: formData });
const data = await response.json();
```

---

## 11. requirements.txt

Generated with:
```
pip freeze > requirements.txt
```
This captures the exact versions of every installed package (including transitive dependencies like `torch`), so the environment can be reproduced exactly by anyone cloning the project.

---

## 12. Decisions Log (Implementation Phase)

- FastAPI serves both the API and the static frontend (single server, single port).
- Semantic matching threshold fixed at `0.6` — favors precision over recall.
- Frontend rebuilt in vanilla HTML/CSS/JS after a Streamlit environment issue, served via FastAPI's `StaticFiles` — functionally equivalent, same design intent (dark theme, card layout, color-coded scores).
- `pip freeze` used for `requirements.txt` to guarantee reproducibility.