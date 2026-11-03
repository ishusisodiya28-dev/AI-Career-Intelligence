
from app.services.career_recommender import ROLE_DATABASE


LEARNING_PATHS = {

    "python": {
        "topics": [
            "Variables and data types",
            "Conditions and loops",
            "Functions and collections",
            "File handling and exceptions",
            "Object-oriented programming"
        ],
        "practice_task": "Build a Python Student Management System.",
        "resource": "Official Python Tutorial",
        "estimated_days": 7
    },

    "sql": {
        "topics": [
            "SELECT, INSERT, UPDATE and DELETE",
            "WHERE, ORDER BY and GROUP BY",
            "Aggregate functions",
            "Joins and subqueries",
            "Database design"
        ],
        "practice_task": "Create a Student Database and write 20 SQL queries.",
        "resource": "SQL learning documentation",
        "estimated_days": 7
    },

    "html": {
        "topics": [
            "HTML document structure",
            "Forms and input elements",
            "Semantic HTML",
            "Tables and links",
            "Accessibility basics"
        ],
        "practice_task": "Build a personal portfolio webpage.",
        "resource": "MDN HTML Guide",
        "estimated_days": 5
    },

    "css": {
        "topics": [
            "Selectors and properties",
            "Box model",
            "Flexbox and Grid",
            "Responsive design",
            "CSS animations"
        ],
        "practice_task": "Create a responsive portfolio website.",
        "resource": "MDN CSS Guide",
        "estimated_days": 7
    },

    "javascript": {
        "topics": [
            "Variables and data types",
            "Functions and arrays",
            "DOM manipulation",
            "Events and promises",
            "Fetch API and async/await"
        ],
        "practice_task": "Build an interactive To-Do List application.",
        "resource": "MDN JavaScript Guide",
        "estimated_days": 7
    },

    "react": {
        "topics": [
            "Components and JSX",
            "Props and state",
            "React Hooks",
            "Event handling",
            "API integration"
        ],
        "practice_task": "Build a React Job Search Dashboard.",
        "resource": "Official React Documentation",
        "estimated_days": 7
    },

    "git": {
        "topics": [
            "Git installation and configuration",
            "Repository creation",
            "Commit and branch",
            "Merge and conflict resolution",
            "GitHub collaboration"
        ],
        "practice_task": "Upload a complete project to GitHub using branches.",
        "resource": "Official Git Documentation",
        "estimated_days": 4
    },

    "fastapi": {
        "topics": [
            "FastAPI application structure",
            "Routes and HTTP methods",
            "Pydantic validation",
            "Database integration",
            "Authentication and JWT"
        ],
        "practice_task": "Build a Student Management REST API.",
        "resource": "Official FastAPI Documentation",
        "estimated_days": 7
    },

    "django": {
        "topics": [
            "Django project structure",
            "Models and ORM",
            "Views and URLs",
            "Templates",
            "Authentication"
        ],
        "practice_task": "Build a Django Student Management Website.",
        "resource": "Official Django Tutorial",
        "estimated_days": 7
    },

    "flask": {
        "topics": [
            "Flask application setup",
            "Routing",
            "Templates",
            "Database integration",
            "REST API development"
        ],
        "practice_task": "Build a Flask Notes API.",
        "resource": "Official Flask Documentation",
        "estimated_days": 7
    },

    "rest api": {
        "topics": [
            "HTTP methods",
            "Status codes",
            "JSON requests and responses",
            "API authentication",
            "API testing"
        ],
        "practice_task": "Develop and test a complete REST API.",
        "resource": "MDN HTTP Documentation",
        "estimated_days": 5
    },

    "mysql": {
        "topics": [
            "Database and table creation",
            "SQL queries",
            "Joins",
            "Constraints and indexes",
            "Database relationships"
        ],
        "practice_task": "Build a College Management Database.",
        "resource": "Official MySQL Documentation",
        "estimated_days": 7
    },

    "postgresql": {
        "topics": [
            "PostgreSQL installation",
            "Database operations",
            "Joins and subqueries",
            "Indexes",
            "Transactions"
        ],
        "practice_task": "Build a Library Management Database.",
        "resource": "Official PostgreSQL Documentation",
        "estimated_days": 7
    },

    "node.js": {
        "topics": [
            "Node.js fundamentals",
            "Modules and npm",
            "Express basics",
            "REST APIs",
            "Database connections"
        ],
        "practice_task": "Build a Node.js Notes API.",
        "resource": "Official Node.js Documentation",
        "estimated_days": 7
    },

    "java": {
        "topics": [
            "Java fundamentals",
            "OOP concepts",
            "Collections framework",
            "Exception handling",
            "JDBC and databases"
        ],
        "practice_task": "Build a Java Banking Management System.",
        "resource": "Official Java Documentation",
        "estimated_days": 7
    },

    "c++": {
        "topics": [
            "C++ syntax and data types",
            "Functions and arrays",
            "Pointers and references",
            "OOP concepts",
            "STL and problem solving"
        ],
        "practice_task": "Build a C++ Library Management System.",
        "resource": "LearnCpp Documentation",
        "estimated_days": 7
    },

    "docker": {
        "topics": [
            "Containers and images",
            "Dockerfile",
            "Docker commands",
            "Docker Compose",
            "Application deployment"
        ],
        "practice_task": "Containerize a Python FastAPI application.",
        "resource": "Official Docker Documentation",
        "estimated_days": 7
    },

    "aws": {
        "topics": [
            "Cloud computing fundamentals",
            "EC2",
            "S3",
            "IAM",
            "Cloud deployment basics"
        ],
        "practice_task": "Deploy a basic web application using AWS.",
        "resource": "AWS Skill Builder",
        "estimated_days": 10
    },

    "machine learning": {
        "topics": [
            "Supervised and unsupervised learning",
            "Data preprocessing",
            "Regression and classification",
            "Model training",
            "Model evaluation"
        ],
        "practice_task": "Build a Student Performance Prediction Model.",
        "resource": "Scikit-learn User Guide",
        "estimated_days": 10
    },

    "deep learning": {
        "topics": [
            "Neural network fundamentals",
            "Activation functions",
            "Loss and optimization",
            "Training and validation",
            "Model evaluation"
        ],
        "practice_task": "Build a basic image classification model.",
        "resource": "PyTorch Tutorials",
        "estimated_days": 10
    },

    "scikit-learn": {
        "topics": [
            "Dataset preparation",
            "Train-test split",
            "Classification algorithms",
            "Regression algorithms",
            "Model evaluation"
        ],
        "practice_task": "Build a classification project using Scikit-learn.",
        "resource": "Official Scikit-learn Documentation",
        "estimated_days": 7
    },

    "pandas": {
        "topics": [
            "Series and DataFrames",
            "Reading CSV files",
            "Data cleaning",
            "Filtering and grouping",
            "Data analysis"
        ],
        "practice_task": "Analyze a real-world sales dataset.",
        "resource": "Official Pandas Documentation",
        "estimated_days": 5
    },

    "numpy": {
        "topics": [
            "NumPy arrays",
            "Array operations",
            "Indexing and slicing",
            "Mathematical functions",
            "Broadcasting"
        ],
        "practice_task": "Perform numerical analysis using NumPy.",
        "resource": "Official NumPy Documentation",
        "estimated_days": 5
    },

    "opencv": {
        "topics": [
            "Image loading and display",
            "Image transformations",
            "Video processing",
            "Object tracking basics",
            "Image analysis"
        ],
        "practice_task": "Build a webcam-based object detection demo.",
        "resource": "Official OpenCV Documentation",
        "estimated_days": 7
    },

    "computer vision": {
        "topics": [
            "Image processing fundamentals",
            "Image classification",
            "Object detection",
            "Image segmentation",
            "Model evaluation"
        ],
        "practice_task": "Build a simple computer vision application.",
        "resource": "OpenCV and PyTorch Tutorials",
        "estimated_days": 10
    },

    "yolo": {
        "topics": [
            "Object detection fundamentals",
            "YOLO architecture overview",
            "Dataset preparation",
            "Model inference",
            "Object tracking"
        ],
        "practice_task": "Build a real-time vehicle detection system.",
        "resource": "Ultralytics Documentation",
        "estimated_days": 7
    },

    "power bi": {
        "topics": [
            "Power BI interface",
            "Data import",
            "Data cleaning",
            "DAX fundamentals",
            "Dashboard creation"
        ],
        "practice_task": "Create an interactive sales dashboard.",
        "resource": "Microsoft Learn Power BI",
        "estimated_days": 7
    },

    "excel": {
        "topics": [
            "Excel formulas",
            "Sorting and filtering",
            "Lookup functions",
            "Pivot tables",
            "Charts and dashboards"
        ],
        "practice_task": "Create an Excel-based sales report.",
        "resource": "Microsoft Excel Training",
        "estimated_days": 5
    },

    "tableau": {
        "topics": [
            "Data connections",
            "Charts and visualizations",
            "Filters",
            "Calculated fields",
            "Dashboard development"
        ],
        "practice_task": "Create an interactive business dashboard.",
        "resource": "Tableau Learning Resources",
        "estimated_days": 7
    },

    "linux": {
        "topics": [
            "Linux commands",
            "File and directory management",
            "Permissions",
            "Shell scripting",
            "Process management"
        ],
        "practice_task": "Create a Linux system monitoring script.",
        "resource": "Linux Documentation",
        "estimated_days": 7
    }
}


def generate_learning_roadmap(candidate_skills, job_role):

    # Find selected role
    role = next(
        (
            item for item in ROLE_DATABASE
            if item["role"].casefold() == job_role.strip().casefold()
        ),
        None
    )

    if role is None:
        raise ValueError("Selected job role not found.")

    # Normalize candidate skills
    candidate_set = {
        skill.strip().casefold()
        for skill in candidate_skills
        if skill.strip()
    }

    required_skills = role["skills"]

    # Available and missing skills
    matched_skills = [
        skill for skill in required_skills
        if skill.casefold() in candidate_set
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill.casefold() not in candidate_set
    ]

    roadmap_weeks = []

    total_days = 0

    # Create one learning week for each missing skill
    for week_number, skill in enumerate(missing_skills, start=1):

        learning_data = LEARNING_PATHS.get(
            skill.casefold(),
            {
                "topics": [
                    f"Understand {skill} fundamentals",
                    f"Learn important concepts of {skill}",
                    f"Practice {skill} with examples",
                    f"Build a practical application using {skill}"
                ],
                "practice_task": (
                    f"Build a small practical project using {skill}."
                ),
                "resource": f"{skill} official documentation",
                "estimated_days": 7
            }
        )

        total_days += learning_data["estimated_days"]

        roadmap_weeks.append({

            "week": week_number,

            "skill_to_learn": skill,

            "estimated_days": learning_data["estimated_days"],

            "learning_topics": learning_data["topics"],

            "practice_task": learning_data["practice_task"],

            "recommended_resource": learning_data["resource"]

        })

    if not missing_skills:
        status = "All required role skills detected"
        recommendation = (
            "You have matched all predefined technical skills "
            "for this role. Focus on advanced projects, "
            "interview practice and practical experience."
        )
    else:
        status = "Learning required"
        recommendation = (
            "Complete the learning weeks in sequence. "
            "Build the suggested practical projects and "
            "update your skills after gaining real experience."
        )

    return {

        "job_role": role["role"],

        "career_level": role["level"],

        "status": status,

        "available_skills": matched_skills,

        "missing_skills": missing_skills,

        "total_missing_skills": len(missing_skills),

        "estimated_duration_weeks": len(roadmap_weeks),

        "estimated_duration_days": total_days,

        "weekly_learning_roadmap": roadmap_weeks,

        "final_capstone_project": (
            f"Build an end-to-end project demonstrating "
            f"your knowledge of {role['role']}."
        ),

        "recommendation": recommendation,

        "note": (
            "This is a rule-based learning plan. "
            "Estimated durations are planning estimates, "
            "not guaranteed completion times."
        )

    }
