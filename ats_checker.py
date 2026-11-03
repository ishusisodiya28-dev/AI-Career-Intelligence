import re

from app.services.resume_parser import extract_skills


SECTION_PATTERNS = {
    "education": [
        r"\beducation\b",
        r"\bacademic record\b",
        r"\bprofessional qualifications\b"
    ],
    "skills": [
        r"\btechnical skills\b",
        r"\bcore skills\b",
        r"\bit skills\b",
        r"\bskills\b"
    ],
    "projects": [
        r"\bprojects?\b",
        r"\bminor project\b",
        r"\bmajor project\b"
    ],
    "experience": [
        r"\bwork experience\b",
        r"\bprofessional experience\b",
        r"\binternships?\b"
    ],
    "summary": [
        r"\bcareer objective\b",
        r"\bprofessional summary\b",
        r"\bprofile summary\b",
        r"\bobjective\b"
    ],
    "certifications": [
        r"\bcertifications?\b",
        r"\bcourses\b",
        r"\blicenses and certifications\b"
    ]
}


def evaluate_ats(resume_text, job_description):

    if not resume_text.strip():
        raise ValueError("Resume text is empty")

    checks = []
    suggestions = []
    score = 0

    def add_check(name, passed, points, suggestion=None):

        nonlocal score

        if passed:
            score += points
            status = "Passed"
        else:
            status = "Needs Improvement"

            if suggestion:
                suggestions.append(suggestion)

        checks.append({
            "check": name,
            "status": status,
            "points_earned": points if passed else 0,
            "maximum_points": points
        })

    # 1. Email check (8 points)
    email_found = bool(re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        resume_text
    ))

    add_check(
        "Email Address",
        email_found,
        8,
        "Add a valid email address."
    )

    # 2. Phone check (7 points)
    phone_found = bool(re.search(
        r"(?<!\d)(?:\+?91[\s-]?)?[6-9](?:[\s-]?\d){9}(?!\d)",
        resume_text
    ))

    add_check(
        "Phone Number",
        phone_found,
        7,
        "Add a valid contact number."
    )

    # 3. Section checks
    for section, patterns in SECTION_PATTERNS.items():

        found = any(
            re.search(pattern, resume_text, re.IGNORECASE)
            for pattern in patterns
        )

        points = {
            "education": 8,
            "skills": 8,
            "projects": 8,
            "experience": 6,
            "summary": 5,
            "certifications": 3
        }[section]

        add_check(
            section.capitalize() + " Section",
            found,
            points,
            f"Consider adding a clearly labelled {section} section."
        )

    # 4. Job keyword analysis (35 points)
    available_skills = set(
        extract_skills(resume_text)
    )

    required_skills = set(
        extract_skills(job_description)
    )

    matched_skills = sorted(
        available_skills.intersection(required_skills)
    )

    missing_skills = sorted(
        required_skills.difference(available_skills)
    )

    if required_skills:

        keyword_percentage = (
            len(matched_skills) /
            len(required_skills)
        ) * 100

        keyword_points = round(
            35 * keyword_percentage / 100,
            2
        )

    else:

        keyword_percentage = None
        keyword_points = 0

    score += keyword_points

    checks.append({
        "check": "Job Description Keywords",
        "status": (
            "Passed"
            if keyword_percentage == 100
            else "Needs Improvement"
        ),
        "points_earned": keyword_points,
        "maximum_points": 35
    })

    if missing_skills:
        suggestions.append(
            "Review these missing job skills: "
            + ", ".join(missing_skills)
        )

    if not required_skills:
        suggestions.append(
            "No recognized technical skills were found "
            "in the job description."
        )

    # 5. Resume length check (7 points)
    words = resume_text.split()
    word_count = len(words)

    if 150 <= word_count <= 1000:
        length_points = 7

    elif 80 <= word_count <= 1300:
        length_points = 4

    else:
        length_points = 1

    score += length_points

    checks.append({
        "check": "Resume Length",
        "status": (
            "Passed" if length_points == 7
            else "Needs Improvement"
        ),
        "points_earned": length_points,
        "maximum_points": 7
    })

    # 6. Readability check (5 points)
    non_empty_lines = [
        line.strip()
        for line in resume_text.splitlines()
        if line.strip()
    ]

    readable = (
        len(non_empty_lines) >= 8
        and word_count >= 80
    )

    add_check(
        "Readable Resume Text",
        readable,
        5,
        "Use clear text, headings and readable formatting."
    )

    ats_score = round(score, 2)

    # Suggestions for improvement
    if not suggestions:
        suggestions.append(
            "Your resume passed all checks in this basic analysis."
        )

    return {
        "ats_compatibility_score": ats_score,
        "word_count": word_count,
        "keyword_match_percentage": (
            round(keyword_percentage, 2)
            if keyword_percentage is not None
            else None
        ),
        "required_keywords": sorted(required_skills),
        "matched_keywords": matched_skills,
        "missing_keywords": missing_skills,
        "checks": checks,
        "suggestions": suggestions,
        "note": (
            "This is a rule-based ATS readiness estimate, "
            "not a score from a commercial ATS platform."
        )
    }