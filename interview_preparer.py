
from app.services.career_recommender import ROLE_DATABASE


QUESTION_BANK = {
    "Python": {
        "question": "What are the differences between a list and a tuple in Python?",
        "answer": "A list is mutable, which means its elements can be modified after creation. A tuple is immutable. Lists use square brackets and tuples generally use parentheses.",
        "difficulty": "Easy"
    },
    "Java": {
        "question": "What are the four main pillars of Object-Oriented Programming?",
        "answer": "The four pillars are Encapsulation, Inheritance, Polymorphism and Abstraction. They help organize code into reusable and maintainable structures.",
        "difficulty": "Medium"
    },
    "C++": {
        "question": "Explain the four pillars of Object-Oriented Programming in C++.",
        "answer": "Encapsulation combines data and methods, Inheritance allows code reuse, Polymorphism supports multiple forms of behavior, and Abstraction hides implementation details.",
        "difficulty": "Medium"
    },
    "HTML": {
        "question": "What are semantic HTML elements?",
        "answer": "Semantic elements clearly describe their meaning, such as header, footer, nav, main, article and section. They improve accessibility and document structure.",
        "difficulty": "Easy"
    },
    "CSS": {
        "question": "Explain the CSS Box Model.",
        "answer": "The CSS Box Model consists of content, padding, border and margin. These properties control an element's size and spacing.",
        "difficulty": "Easy"
    },
    "JavaScript": {
        "question": "What is the difference between var, let and const?",
        "answer": "Var is function-scoped, let is block-scoped and can be reassigned, while const is block-scoped and cannot be reassigned.",
        "difficulty": "Easy"
    },
    "React": {
        "question": "What is the difference between props and state in React?",
        "answer": "Props are passed from parent components and are read-only. State is managed inside a component and can change over time.",
        "difficulty": "Medium"
    },
    "Node.js": {
        "question": "What is Node.js and why is it used?",
        "answer": "Node.js is a JavaScript runtime built on Chrome's V8 engine. It is commonly used for building server-side applications and APIs.",
        "difficulty": "Medium"
    },
    "SQL": {
        "question": "What is the difference between INNER JOIN and LEFT JOIN?",
        "answer": "INNER JOIN returns matching rows from both tables. LEFT JOIN returns all rows from the left table and matching rows from the right table.",
        "difficulty": "Easy"
    },
    "MySQL": {
        "question": "What is the difference between a primary key and a foreign key?",
        "answer": "A primary key uniquely identifies a record in a table. A foreign key refers to a key in another table and establishes a relationship.",
        "difficulty": "Easy"
    },
    "SQLite": {
        "question": "What is SQLite and how is it different from a database server?",
        "answer": "SQLite is a lightweight embedded relational database that stores data in a file. It does not require a separate database server process.",
        "difficulty": "Easy"
    },
    "PostgreSQL": {
        "question": "What is an index in PostgreSQL?",
        "answer": "An index is a data structure that can speed up data retrieval. It can improve read performance but may add storage and write overhead.",
        "difficulty": "Medium"
    },
    "FastAPI": {
        "question": "What is FastAPI and what are its main advantages?",
        "answer": "FastAPI is a Python framework for building APIs. It supports type hints, request validation through Pydantic, automatic OpenAPI documentation and asynchronous endpoints.",
        "difficulty": "Medium"
    },
    "Django": {
        "question": "Explain the MVT architecture in Django.",
        "answer": "MVT stands for Model, View and Template. Model manages data, View handles request logic, and Template controls presentation.",
        "difficulty": "Medium"
    },
    "Flask": {
        "question": "What is Flask and how does routing work?",
        "answer": "Flask is a lightweight Python web framework. Routes map URL paths to Python functions that handle incoming requests.",
        "difficulty": "Easy"
    },
    "REST API": {
        "question": "Explain the GET, POST, PUT and DELETE HTTP methods.",
        "answer": "GET retrieves resources, POST creates resources, PUT updates or replaces a resource, and DELETE removes a resource.",
        "difficulty": "Easy"
    },
    "Git": {
        "question": "What is the difference between Git and GitHub?",
        "answer": "Git is a version control system used to track code changes. GitHub is an online platform for hosting Git repositories and collaborating.",
        "difficulty": "Easy"
    },
    "Docker": {
        "question": "What is the difference between a Docker image and a container?",
        "answer": "An image is a packaged template containing application dependencies. A container is a running or stopped instance of an image.",
        "difficulty": "Medium"
    },
    "AWS": {
        "question": "What are Amazon EC2 and Amazon S3?",
        "answer": "EC2 provides virtual computing instances. S3 is an object storage service used to store files and other data.",
        "difficulty": "Medium"
    },
    "Machine Learning": {
        "question": "What is the difference between supervised and unsupervised learning?",
        "answer": "Supervised learning uses labelled data to learn predictions. Unsupervised learning identifies patterns in data without provided labels.",
        "difficulty": "Medium"
    },
    "Deep Learning": {
        "question": "What is an artificial neural network?",
        "answer": "An artificial neural network is a computational model made of interconnected layers of nodes. It learns patterns by adjusting weights during training.",
        "difficulty": "Medium"
    },
    "Scikit-learn": {
        "question": "What is Scikit-learn used for?",
        "answer": "Scikit-learn is a Python library for machine learning. It provides tools for classification, regression, clustering, preprocessing and model evaluation.",
        "difficulty": "Easy"
    },
    "Pandas": {
        "question": "What is a DataFrame in Pandas?",
        "answer": "A DataFrame is a two-dimensional labelled data structure with rows and columns. It supports data cleaning, filtering and analysis.",
        "difficulty": "Easy"
    },
    "NumPy": {
        "question": "What is a NumPy array?",
        "answer": "A NumPy array is an efficient multidimensional array used for numerical computing. It supports vectorized operations and mathematical functions.",
        "difficulty": "Easy"
    },
    "Computer Vision": {
        "question": "What is Computer Vision?",
        "answer": "Computer Vision is a field of AI that enables computers to interpret images and videos using image processing and machine learning techniques.",
        "difficulty": "Easy"
    },
    "OpenCV": {
        "question": "What is OpenCV used for?",
        "answer": "OpenCV is a computer vision library used for image processing, object tracking, video analysis and feature detection.",
        "difficulty": "Easy"
    },
    "YOLO": {
        "question": "What is YOLO in object detection?",
        "answer": "YOLO stands for You Only Look Once. It is a family of object detection models designed to identify objects and predict their locations in images.",
        "difficulty": "Medium"
    },
    "Power BI": {
        "question": "What is the difference between a measure and a calculated column in Power BI?",
        "answer": "A calculated column is evaluated for each row and stored in the model. A measure is calculated dynamically based on the current filter context.",
        "difficulty": "Medium"
    },
    "Excel": {
        "question": "What is the purpose of VLOOKUP in Excel?",
        "answer": "VLOOKUP searches for a value in the first column of a table and returns a corresponding value from another column.",
        "difficulty": "Easy"
    },
    "Linux": {
        "question": "What is the difference between absolute and relative file paths in Linux?",
        "answer": "An absolute path starts from the root directory. A relative path describes a location from the current working directory.",
        "difficulty": "Easy"
    },
    "Tableau": {
        "question": "What is Tableau used for?",
        "answer": "Tableau is a data visualization platform used to create interactive charts, dashboards and reports from data sources.",
        "difficulty": "Easy"
    }
}


PROJECT_QUESTIONS = [
    {
        "question": "Explain one project you have developed. What problem does it solve?",
        "sample_answer": "Use this structure: Project name, problem statement, technologies used, your contribution and final outcome. Mention only work you actually completed.",
        "difficulty": "Medium"
    },
    {
        "question": "What was the biggest technical challenge in your project?",
        "sample_answer": "Describe the challenge, why it occurred, the steps you took to solve it and what you learned.",
        "difficulty": "Medium"
    }
]


BEHAVIORAL_QUESTIONS = [
    {
        "question": "Tell me about yourself.",
        "sample_answer": "Start with your education, technical interests, programming skills, one relevant project and the type of role you are seeking. Keep it within 60 to 90 seconds.",
        "difficulty": "Easy"
    },
    {
        "question": "How do you learn a new technology?",
        "sample_answer": "Explain that you first understand the fundamentals, follow documentation, build a small practical project and then improve it through testing.",
        "difficulty": "Easy"
    },
    {
        "question": "How do you handle a difficult task or deadline?",
        "sample_answer": "Explain how you divide the task into smaller steps, prioritize important work, monitor progress and communicate blockers.",
        "difficulty": "Medium"
    }
]


def prepare_interview(candidate_skills, job_role):

    role = next(
        (
            item for item in ROLE_DATABASE
            if item["role"].casefold() == job_role.strip().casefold()
        ),
        None
    )

    if role is None:
        raise ValueError("Please select a valid job role.")

    question_bank = {
        name.casefold(): data
        for name, data in QUESTION_BANK.items()
    }

    # Prefer skills required by the selected role
    technical_skills = []
    used_skills = set()

    for skill in role["skills"] + candidate_skills:

        normalized = skill.casefold()

        if normalized in used_skills:
            continue

        used_skills.add(normalized)

        question_data = question_bank.get(normalized)

        if question_data:
            technical_skills.append({
                "category": "Technical",
                "skill": skill,
                "question": question_data["question"],
                "sample_answer": question_data["answer"],
                "difficulty": question_data["difficulty"]
            })

        if len(technical_skills) >= 6:
            break

    project_questions = [
        {
            "category": "Project",
            **item
        }
        for item in PROJECT_QUESTIONS
    ]

    behavioral_questions = [
        {
            "category": "Behavioral",
            **item
        }
        for item in BEHAVIORAL_QUESTIONS
    ]

    return {
        "job_role": role["role"],
        "career_level": role["level"],
        "technical_questions": technical_skills,
        "project_questions": project_questions,
        "behavioral_questions": behavioral_questions,
        "total_questions": (
            len(technical_skills)
            + len(project_questions)
            + len(behavioral_questions)
        )
    }
