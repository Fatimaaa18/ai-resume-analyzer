def generate_suggestions(match_score: float, missing_skills: list, ats_issues: list) -> list:
    suggestions = []

    if match_score < 50:
        suggestions.append("Your resume has a low match score for this job. Consider tailoring your resume more closely to the job description.")
    elif match_score < 75:
        suggestions.append("Your resume has a moderate match score. Adding a few more relevant skills could improve it.")
    else:
        suggestions.append("Your resume matches this job description well.")

    if len(missing_skills) > 0:
        skills_text = ", ".join(missing_skills)
        suggestions.append(f"Consider adding these skills if you have relevant experience: {skills_text}.")

    if len(ats_issues) > 0:
        suggestions.append("Your resume has formatting issues that may affect ATS readability:")
        for issue in ats_issues:
            suggestions.append(f"- {issue}")
    else:
        suggestions.append("Your resume format appears ATS-friendly.")

    return suggestions