SKILLS_LIST = {
    "python", "java", "javascript", "sql", "html", "css",
    "fastapi", "flask", "django", "react", "node",
    "machine learning", "deep learning", "nlp",
    "data structures", "algorithms", "rest api",
    "postgresql", "mysql", "mongodb",
    "git", "github", "docker", "aws",
    "pandas", "numpy", "tensorflow", "pytorch"
}
def extract_skills(cleaned_text: str) -> set:
    found_skills = set()
    for skill in SKILLS_LIST:
        if skill in cleaned_text:
            found_skills.add(skill)
    return found_skills