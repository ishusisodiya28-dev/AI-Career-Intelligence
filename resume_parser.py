
import re


SKILL_PATTERNS = {
    "Python": r"\bpython\b",
    "Java": r"\bjava\b",
    "C++": r"(?<!\w)c\+\+(?!\w)",
    "C": r"(?<![a-z0-9_+#])c(?![a-z0-9_+#])",
    "JavaScript": r"\bjavascript\b",
    "SQL": r"\bsql\b",
    "HTML": r"\bhtml\b",
    "CSS": r"\bcss\b",
    "React": r"\breact\b",
    "Node.js": r"\bnode\.?js\b",
    "FastAPI": r"\bfastapi\b",
    "Django": r"\bdjango\b",
    "Flask": r"\bflask\b",
    "MySQL": r"\bmysql\b",
    "SQLite": r"\bsqlite\b",
    "MongoDB": r"\bmongodb\b",
    "PostgreSQL": r"\bpostgresql\b",
    "Machine Learning": r"\bmachine learning\b",
    "Deep Learning": r"\bdeep learning\b",
    "NLP": r"\bnlp\b",
    "Computer Vision": r"\bcomputer vision\b",
    "OpenCV": r"\bopencv\b",
    "YOLO": r"\byolo\b",
    "Pandas": r"\bpandas\b",
    "NumPy": r"\bnumpy\b",
    "Scikit-learn": r"\bscikit.learn\b",
    "Git": r"\bgit\b",
    "GitHub": r"\bgithub\b",
    "Docker": r"\bdocker\b",
    "AWS": r"\baws\b",
    "Power BI": r"\bpower bi\b",
    "Excel": r"\bexcel\b",
    "Tableau": r"\btableau\b",
    "REST API": r"\brest api\b",
    "Linux": r"\blinux\b"
}


SECTION_ALIASES = {
    "education": [
        "education",
        "academic record",
        "academic qualifications",
        "educational qualifications",
        "professional qualifications"
    ],
    "projects": [
        "projects",
        "minor project",
        "minorproject",
        "major project",
        "personal projects",
        "academic projects",
        "key projects"
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "internship",
        "internships"
    ],
    "certifications": [
        "certifications",
        "certificates",
        "courses",
        "licenses and certifications"
    ],
    "skills": [
        "skills",
        "technical skills",
        "technical expertise",
        "key skills",
        "it skills core skills"
    ],
    "career_objective": [
        "career objective",
        "objective",
        "professional summary",
        "profile summary"
    ]
}


STOP_HEADINGS = [
    "extracurricular activities",
    "strengths",
    "area of improvement",
    "hobbies",
    "personal details",
    "personal information",
    "declaration",
    "date of birth",
    "gender",
    "nationality",
    "marital status"
]


def normalize_heading(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def clean_lines(text):

    lines = []

    for line in text.splitlines():

        line = line.strip()

        line = re.sub(
            r"^[\s•●▪◆➢➤⮚\-*]+",
            "",
            line
        )

        if line:
            lines.append(line)

    return lines


def detect_heading(line):

    if ":" in line:
        label, content = line.split(":", 1)
    else:
        label = line
        content = ""

    normalized = normalize_heading(label)

    for section, aliases in SECTION_ALIASES.items():

        normalized_aliases = [
            normalize_heading(alias)
            for alias in aliases
        ]

        if normalized in normalized_aliases:
            return section, content.strip(), False

    normalized_stops = [
        normalize_heading(item)
        for item in STOP_HEADINGS
    ]

    if normalized in normalized_stops:
        return None, "", True

    return None, "", False


def extract_sections(lines):

    sections = {
        section: []
        for section in SECTION_ALIASES
    }

    current_section = None

    for line in lines:

        heading, inline_content, is_stop = detect_heading(line)

        if heading:

            current_section = heading

            if inline_content:
                sections[current_section].append(inline_content)

            continue

        if is_stop:

            current_section = None
            continue

        if current_section:
            sections[current_section].append(line)

    return sections


def extract_email(text):

    pattern = (
        r"[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}"
    )

    match = re.search(pattern, text)

    return match.group(0) if match else None


def extract_phone(text):

    pattern = (
        r"(?<!\d)(?:\+?91[\s-]?)?"
        r"[6-9](?:[\s-]?\d){9}(?!\d)"
    )

    match = re.search(pattern, text)

    if match:
        return re.sub(
            r"[\s-]",
            "",
            match.group(0)
        )

    return None


def extract_name(lines):

    for line in lines[:10]:

        if "@" in line:
            continue

        if re.search(r"\d{7,}", line):
            continue

        if normalize_heading(line) in [
            "resume",
            "curriculum vitae",
            "cv"
        ]:
            continue

        if len(line) <= 80:
            return line

    return None


def extract_skills(text):

    found_skills = []

    for skill, pattern in SKILL_PATTERNS.items():

        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills


def extract_education(text, education_lines):

    if education_lines:
        return education_lines[:20]

    keywords = re.compile(
        r"bachelor|b\.?e\.?|b\.?tech|btech|"
        r"master|m\.?e\.?|m\.?tech|diploma|"
        r"10th|12th|class 10|class 12|"
        r"university|college|pursuing|graduation",
        re.IGNORECASE
    )

    return [
        line
        for line in clean_lines(text)
        if keywords.search(line)
    ][:20]


def parse_resume_text(text):

    lines = clean_lines(text)

    sections = extract_sections(lines)

    return {

        "candidate_details": {
            "name": extract_name(lines),
            "email": extract_email(text),
            "phone": extract_phone(text)
        },

        "education": extract_education(
            text,
            sections["education"]
        ),

        "technical_skills": extract_skills(text),

        "projects": sections["projects"][:25],

        "experience": sections["experience"][:25],

        "certifications": sections["certifications"][:20],

        "career_objective": (
            " ".join(sections["career_objective"])[:1000]
            or None
        )
    }
