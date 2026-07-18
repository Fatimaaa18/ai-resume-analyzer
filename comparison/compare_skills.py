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