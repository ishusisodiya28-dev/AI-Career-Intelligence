
from app.services.career_recommender import ROLE_DATABASE


def simulate_what_if(
    candidate_skills,
    job_role,
    additional_skills
):

    # Find selected career role
    role = next(
        (
            item for item in ROLE_DATABASE
            if item["role"].lower() == job_role.strip().lower()
        ),
        None
    )

    if role is None:
        raise ValueError(
            "Job role not found. Please select a valid role."
        )

    required_skills = role["skills"]

    if not required_skills:
        raise ValueError("No required skills configured for this role.")

    # Normalize existing candidate skills
    candidate_skill_set = {
        skill.strip().casefold()
        for skill in candidate_skills
        if skill.strip()
    }

    # Calculate current matched skills
    current_matched = {
        skill for skill in required_skills
        if skill.casefold() in candidate_skill_set
    }

    # Match additional skills against role requirements
    required_skill_map = {
        skill.casefold(): skill
        for skill in required_skills
    }

    projected_matched = set(current_matched)
    accepted_additions = set()
    ignored_skills = []

    for skill in additional_skills:

        normalized = skill.strip().casefold()

        if not normalized:
            continue

        canonical_skill = required_skill_map.get(normalized)

        if canonical_skill:
            projected_matched.add(canonical_skill)

            if canonical_skill not in current_matched:
                accepted_additions.add(canonical_skill)

        else:
            ignored_skills.append(skill.strip())

    # Calculate scores
    total_required = len(required_skills)

    current_score = round(
        len(current_matched) / total_required * 100,
        2
    )

    projected_score = round(
        len(projected_matched) / total_required * 100,
        2
    )

    score_improvement = round(
        projected_score - current_score,
        2
    )

    # Remaining skills
    remaining_skills = sorted(
        set(required_skills) - projected_matched
    )

    return {

        "job_role": role["role"],

        "career_level": role["level"],

        "current_match_score": current_score,

        "projected_match_score": projected_score,

        "score_improvement": score_improvement,

        "total_required_skills": total_required,

        "current_matched_skills": sorted(current_matched),

        "newly_matched_skills": sorted(accepted_additions),

        "projected_matched_skills": sorted(projected_matched),

        "remaining_skills_to_learn": remaining_skills,

        "ignored_skills": sorted(set(ignored_skills)),

        "description": role["description"],

        "note": (
            "This is a hypothetical simulation. "
            "Additional skills are not actually added "
            "to the candidate's resume."
        )

    }
