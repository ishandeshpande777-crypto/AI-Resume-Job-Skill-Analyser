
import re

SKILLS_DATABASE = [
    "python",
    "java",
    "c++",
    "c",
    "sql",
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
    "flask",
    "django",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analysis",
    "excel",
    "power bi",
    "tableau",
    "mongodb",
    "mysql",
    "git",
    "github",
    "communication",
    "teamwork",
    "problem solving",
    "leadership",
    "project management"
]


def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS_DATABASE:
        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


def analyze_skills(resume_skills, job_skills):

    matched = []
    missing = []

    for skill in job_skills:
        if skill in resume_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    if len(job_skills) > 0:
        score = (len(matched) / len(job_skills)) * 100
    else:
        score = 0

    return matched, missing, round(score, 2)




def recommend_skills(missing_skills):

    learning_guide = {
        "python": "Study Python basics, functions, loops and object-oriented programming. Practice by building a calculator or automation tool.",
        "java": "Learn Java syntax, OOP, collections and exception handling. Practice by building a student management system.",
        "sql": "Learn SELECT, JOIN, GROUP BY and database operations. Practice by creating a student database.",
        "html": "Learn HTML elements, forms and semantic structure. Practice by building a personal portfolio page.",
        "css": "Learn selectors, Flexbox, Grid and responsive design. Practice by styling a portfolio website.",
        "javascript": "Learn variables, functions, DOM manipulation and events. Practice by building an interactive to-do list.",
        "react": "Study components, props, state and hooks. Practice by creating a React task manager.",
        "flask": "Learn Flask routes, templates and form handling. Practice by building a simple web application.",
        "django": "Learn Django models, views, templates and URLs. Practice by creating a blog application.",
        "machine learning": "Study supervised learning, classification and model evaluation. Practice by building a simple prediction model.",
        "deep learning": "Learn neural networks, activation functions and model training. Practice by building an image classifier.",
        "artificial intelligence": "Study AI fundamentals, search algorithms and machine learning concepts. Practice by creating a simple chatbot.",
        "data science": "Learn data cleaning, statistics and data visualization. Practice by analysing a public dataset.",
        "data analysis": "Study data cleaning, Excel, Python and visualization. Practice by preparing a sales analysis report.",
        "excel": "Learn formulas, sorting, filtering and pivot tables. Practice by creating a sales dashboard.",
        "power bi": "Learn data modelling, Power Query and dashboards. Practice by building a business performance dashboard.",
        "tableau": "Learn charts, filters and interactive dashboards. Practice by visualizing a sales dataset.",
        "mongodb": "Study collections, documents and CRUD operations. Practice by building a small database application.",
        "mysql": "Learn relational databases, SQL queries and table relationships. Practice by designing a library database.",
        "git": "Learn commits, branches and version control. Practice by tracking a software project.",
        "github": "Learn repositories, pull requests and collaboration. Practice by publishing a project on GitHub.",
        "communication": "Improve verbal and written communication. Practice by presenting a project clearly.",
        "teamwork": "Develop collaboration and task-sharing skills. Practice through a group project.",
        "problem solving": "Practice logical thinking and coding challenges. Solve problems on beginner programming platforms.",
        "leadership": "Develop planning, decision-making and coordination skills. Practice by leading a small team project.",
        "project management": "Learn task planning, milestones and project tracking. Practice by managing a project using a task board."
    }

    recommendations = []

    for skill in missing_skills:
        if skill in learning_guide:
            recommendations.append(
                skill.title() + ": " + learning_guide[skill]
            )
        else:
            recommendations.append(
                "Learn " + skill + " through tutorials and practical projects."
            )

    return recommendations



from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_text_similarity(resume_text, job_text):

    documents = [resume_text, job_text]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    try:
        vectors = vectorizer.fit_transform(documents)

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )

        score = similarity[0][0] * 100

        return round(score, 2)

    except ValueError:
        return 0.0


def check_resume_sections(resume_text):

    section_keywords = {
        "Contact Information": [
            "contact", "contact information", "personal details"
        ],
        "Professional Summary": [
            "summary", "professional summary", "career objective",
            "objective", "profile"
        ],
        "Education": [
            "education", "educational qualifications", "academic qualifications"
        ],
        "Work Experience": [
            "experience", "work experience", "professional experience",
            "employment history"
        ],
        "Skills": [
            "skills", "technical skills", "core skills", "key skills"
        ],
        "Projects": [
            "projects", "academic projects", "personal projects"
        ],
        "Certifications": [
            "certifications", "certificates", "licenses and certifications"
        ]
    }

    # Convert the resume into individual, cleaned lines.
    lines = [
        line.strip().lower().strip(" :#-")
        for line in resume_text.splitlines()
        if line.strip()
    ]

    results = {}

    for section, keywords in section_keywords.items():
        found = False

        for line in lines:
            for keyword in keywords:
                if line == keyword or line.startswith(keyword + ":"):
                    found = True
                    break

            if found:
                break

        results[section] = found

    return results


def calculate_resume_quality(resume_text, resume_skills, resume_sections):

    score = 0
    suggestions = []

    # Check resume length
    word_count = len(resume_text.split())

    if word_count >= 100:
        score += 20
    else:
        suggestions.append(
            "Add more relevant information to your resume."
        )

    # Check important resume sections
    important_sections = [
        "Education",
        "Skills",
        "Projects",
        "Work Experience"
    ]

    for section in important_sections:

        if resume_sections.get(section, False):
            score += 15
        else:
            suggestions.append(
                "Consider adding a " + section + " section."
            )

    # Check recognized skills
    if len(resume_skills) >= 5:
        score += 20
    elif len(resume_skills) >= 3:
        score += 10
        suggestions.append(
            "Include more relevant skills where applicable."
        )
    else:
        suggestions.append(
            "Add relevant technical and professional skills."
        )

    score = min(score, 100)

    if not suggestions:
        suggestions.append(
            "Your resume contains the basic sections checked by this tool."
        )

    return score, suggestions
