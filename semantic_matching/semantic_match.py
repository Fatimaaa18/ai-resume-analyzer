from sentence_transformers import SentenceTransformer , util
model = SentenceTransformer('all-MiniLM-L6-v2')
def get_semantic_matches(resume_skills: set , jd_skills: set , threshold: float = 0.6) -> set:
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
