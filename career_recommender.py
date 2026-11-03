
ROLE_DATABASE = [
    {
        "role": "Python Backend Developer",
        "skills": [
            "Python", "SQL", "FastAPI", "Django",
            "Flask", "REST API", "MySQL", "Git"
        ],
        "level": "Beginner to Intermediate",
        "description": "Develop backend applications, APIs and database systems."
    },
    {
        "role": "Frontend Developer",
        "skills": [
            "HTML", "CSS", "JavaScript", "React", "Git"
        ],
        "level": "Beginner",
        "description": "Build responsive and interactive websites."
    },
    {
        "role": "Full Stack Developer",
        "skills": [
            "HTML", "CSS", "JavaScript", "React",
            "Node.js", "Python", "SQL", "REST API"
        ],
        "level": "Intermediate",
        "description": "Develop both frontend and backend applications."
    },
    {
        "role": "Data Analyst",
        "skills": [
            "Python", "SQL", "Excel", "Power BI",
            "Tableau", "Pandas", "NumPy"
        ],
        "level": "Beginner to Intermediate",
        "description": "Analyze data and generate useful business insights."
    },
    {
        "role": "Data Scientist",
        "skills": [
            "Python", "SQL", "Pandas", "NumPy",
            "Scikit-learn", "Machine Learning"
        ],
        "level": "Intermediate",
        "description": "Build statistical and machine learning solutions."
    },
    {
        "role": "Machine Learning Engineer",
        "skills": [
            "Python", "Machine Learning", "Deep Learning",
            "Scikit-learn", "Docker", "AWS"
        ],
        "level": "Intermediate to Advanced",
        "description": "Develop and deploy machine learning models."
    },
    {
        "role": "Computer Vision Engineer",
        "skills": [
            "Python", "OpenCV", "YOLO",
            "Computer Vision", "Deep Learning"
        ],
        "level": "Intermediate",
        "description": "Build AI systems that understand images and videos."
    },
    {
        "role": "C++ Developer",
        "skills": [
            "C++", "SQL", "Git", "Linux"
        ],
        "level": "Beginner to Intermediate",
        "description": "Develop software using C++ programming."
    },
    {
        "role": "Java Backend Developer",
        "skills": [
            "Java", "SQL", "MySQL", "REST API", "Git"
        ],
        "level": "Beginner to Intermediate",
        "description": "Create server-side applications using Java."
    },
    {
        "role": "DevOps Engineer",
        "skills": [
            "Linux", "Docker", "AWS", "Git", "Python"
        ],
        "level": "Intermediate",
        "description": "Manage deployment, automation and infrastructure."
    },
    {
        "role": "QA Automation Engineer",
        "skills": [
            "Python", "Java", "SQL", "Git"
        ],
        "level": "Beginner to Intermediate",
        "description": "Automate software testing and quality checks."
    },
    {
        "role": "SQL Developer",
        "skills": [
            "SQL", "MySQL", "PostgreSQL", "Python"
        ],
        "level": "Beginner",
        "description": "Design databases and write efficient SQL queries."
    }
]


def recommend_careers(candidate_skills):

    normalized_skills = {
        skill.strip().lower()
        for skill in candidate_skills
    }

    recommendations = []

    for role in ROLE_DATABASE:

        required_skills = set(role["skills"])

        matched_skills = sorted([
            skill for skill in required_skills
            if skill.lower() in normalized_skills
        ])

        missing_skills = sorted(
            required_skills - set(matched_skills)
        )

        total_skills = len(required_skills)

        match_score = round(
            len(matched_skills) / total_skills * 100,
            2
        )

        recommendations.append({

            "job_role": role["role"],

            "match_score": match_score,

            "level": role["level"],

            "description": role["description"],

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "skills_to_learn": missing_skills,

            "recommendation_reason": (
                f"{len(matched_skills)} out of "
                f"{total_skills} required skills matched."
            )

        })

    # Highest matching roles first
    recommendations.sort(
        key=lambda item: (
            item["match_score"],
            len(item["matched_skills"])
        ),
        reverse=True
    )

    # Return top five recommendations
    return recommendations[:5]
