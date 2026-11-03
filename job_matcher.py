from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.resume_parser import extract_skills


def calculate_job_match(resume_text, job_description):

    if not resume_text or not job_description:
        raise ValueError("Resume and job description are required")

    available_skills = sorted(set(extract_skills(resume_text)))
    required_skills = sorted(set(extract_skills(job_description)))

    available_set = set(available_skills)
    required_set = set(required_skills)

    matched_skills = sorted(
        available_set.intersection(required_set)
    )

    missing_skills = sorted(
        required_set.difference(available_set)
    )

    if required_skills:
        skill_score = (
            len(matched_skills) / len(required_skills)
        ) * 100
    else:
        skill_score = None

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform([
        resume_text,
        job_description
    ])

    text_score = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0] * 100

    if skill_score is not None:
        overall_score = (
            0.60 * skill_score +
            0.40 * text_score
        )
    else:
        overall_score = text_score

    return {
        "overall_match_score": round(float(overall_score), 2),
        "skill_match_score": (
            round(float(skill_score), 2)
            if skill_score is not None else None
        ),
        "text_similarity_score": round(float(text_score), 2),
        "available_skills": available_skills,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "partially_matched_skills": []
    }