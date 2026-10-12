"""
analyzer.py - Skill Analysis and Learning Roadmap Engine for SkillBridge AI
Provides skill taxonomy, extraction, matching algorithms, and roadmap generation.
Works completely offline without external API keys using built-in knowledge bases.
"""

import re
from typing import Dict, List, Set, Any, Tuple

# Comprehensive taxonomy of in-demand tech skills
SKILL_TAXONOMY: Dict[str, Dict[str, Any]] = {
    # Programming Languages
    "python": {
        "name": "Python",
        "category": "Programming Languages",
        "aliases": ["python", "python3", "py"],
        "difficulty": "Beginner",
        "priority": "High",
        "description": "High-level, versatile programming language popular for web, data, and AI.",
        "resource": "Official Python Tutorial (docs.python.org) & Automate the Boring Stuff",
        "project_idea": "Build a command-line tool or automated web scraper.",
        "duration_weeks": 2,
    },
    "javascript": {
        "name": "JavaScript",
        "category": "Programming Languages",
        "aliases": ["javascript", "js", "es6", "ecmascript"],
        "difficulty": "Beginner",
        "priority": "High",
        "description": "Core language of the web for client-side and full-stack development.",
        "resource": "MDN Web Docs JavaScript Guide & javascript.info",
        "project_idea": "Create an interactive browser dashboard with local storage.",
        "duration_weeks": 2,
    },
    "typescript": {
        "name": "TypeScript",
        "category": "Programming Languages",
        "aliases": ["typescript", "ts"],
        "difficulty": "Intermediate",
        "priority": "High",
        "description": "Typed superset of JavaScript that scales for large production applications.",
        "resource": "TypeScript Handbook (typescriptlang.org)",
        "project_idea": "Refactor a JavaScript utility or app with strict typing and interfaces.",
        "duration_weeks": 1.5,
    },
    "java": {
        "name": "Java",
        "category": "Programming Languages",
        "aliases": ["java", "core java", "java 17", "java 21"],
        "difficulty": "Intermediate",
        "priority": "High",
        "description": "Object-oriented language widely used in enterprise backends and Android.",
        "resource": "Oracle Java Tutorials & Mooc.fi Java Programming",
        "project_idea": "Build an object-oriented inventory management system.",
        "duration_weeks": 3,
    },
    "csharp": {
        "name": "C#",
        "category": "Programming Languages",
        "aliases": ["c#", "csharp", "c sharp", ".net c#"],
        "difficulty": "Intermediate",
        "priority": "High",
        "description": "Modern language developed by Microsoft for web APIs, desktop, and game dev.",
        "resource": "Microsoft Learn C# Documentation",
        "project_idea": "Develop a REST API with ASP.NET Core and Entity Framework.",
        "duration_weeks": 2.5,
    },
    "cpp": {
        "name": "C++",
        "category": "Programming Languages",
        "aliases": ["c++", "cpp"],
        "difficulty": "Advanced",
        "priority": "Medium",
        "description": "High-performance language for systems, game engines, and embedded software.",
        "resource": "learncpp.com tutorials",
        "project_idea": "Build a memory-efficient cache or custom data structure library.",
        "duration_weeks": 4,
    },
    "go": {
        "name": "Go (Golang)",
        "category": "Programming Languages",
        "aliases": ["golang", "go lang"],
        "difficulty": "Intermediate",
        "priority": "High",
        "description": "Fast, statically typed language created by Google for cloud and microservices.",
        "resource": "Tour of Go (go.dev/tour)",
        "project_idea": "Build a concurrent web crawler or lightweight microservice.",
        "duration_weeks": 2,
    },
    "rust": {
        "name": "Rust",
        "category": "Programming Languages",
        "aliases": ["rust", "rustlang"],
        "difficulty": "Advanced",
        "priority": "Medium",
        "description": "Memory-safe systems programming language with zero-cost abstractions.",
        "resource": "The Rust Book (doc.rust-lang.org/book)",
        "project_idea": "Build a high-performance CLI tool or file parser.",
        "duration_weeks": 3.5,
    },
    "sql": {
        "name": "SQL",
        "category": "Databases & Data",
        "aliases": ["sql", "structured query language", "rdbms"],
        "difficulty": "Beginner",
        "priority": "High",
        "description": "Standard query language for relational database management and data manipulation.",
        "resource": "SQLBolt & Mode Analytics SQL Tutorial",
        "project_idea": "Design an e-commerce database schema and write complex multi-table joins.",
        "duration_weeks": 1.5,
    },
    "html_css": {
        "name": "HTML & CSS",
        "category": "Frontend Development",
        "aliases": ["html", "css", "html5", "css3", "html/css"],
        "difficulty": "Beginner",
        "priority": "High",
        "description": "Building blocks of web structure, semantic markup, and modern styling.",
        "resource": "MDN Learn Web Development",
        "project_idea": "Design a responsive, accessible portfolio page from scratch.",
        "duration_weeks": 1.5,
    },

    # Frontend Frameworks & Libraries
    "react": {
        "name": "React",
        "category": "Frontend Development",
        "aliases": ["react", "react.js", "reactjs"],
        "difficulty": "Intermediate",
        "priority": "High",
        "description": "Declarative component-based UI library powering modern single-page apps.",
        "resource": "React.dev official documentation and interactive tutorials",
        "project_idea": "Build a task management kanban board with state management.",
        "duration_weeks": 2.5,
    },
    "nextjs": {
        "name": "Next.js",
        "category": "Frontend Development",
        "aliases": ["next.js", "nextjs", "next"],
        "difficulty": "Intermediate",
        "priority": "High",
        "description": "Full-stack React framework featuring server-side rendering and static generation.",
        "resource": "Next.js Learn Course (nextjs.org/learn)",
        "project_idea": "Create a modern blog or SaaS marketing site with SEO optimization.",
        "duration_weeks": 2,
    },
    "vue": {
        "name": "Vue.js",
        "category": "Frontend Development",
        "aliases": ["vue", "vue.js", "vuejs", "vue3"],
        "difficulty": "Intermediate",
        "priority": "Medium",
        "description": "Progressive, approachable JavaScript framework for building user interfaces.",
        "resource": "Vuejs.org official documentation",
        "project_idea": "Create an interactive expense tracker with dynamic charts.",
        "duration_weeks": 2,
    },
    "angular": {
        "name": "Angular",
        "category": "Frontend Development",
        "aliases": ["angular", "angularjs", "angular 2+"],
        "difficulty": "Advanced",
        "priority": "Medium",
        "description": "Opinionated, enterprise-ready web framework using TypeScript by Google.",
        "resource": "Angular.dev documentation and interactive playground",
        "project_idea": "Build an enterprise employee directory with nested routing.",
        "duration_weeks": 3,
    },
    "tailwind": {
        "name": "Tailwind CSS",
        "category": "Frontend Development",
        "aliases": ["tailwind", "tailwindcss", "tailwind css"],
        "difficulty": "Beginner",
        "priority": "High",
        "description": "Utility-first CSS framework for rapid, custom UI composition.",
        "resource": "Tailwindcss.com official documentation",
        "project_idea": "Recreate a polished landing page interface using utility classes.",
        "duration_weeks": 1,
    },
    "redux": {
        "name": "Redux / State Management",
        "category": "Frontend Development",
        "aliases": ["redux", "redux toolkit", "zustand", "state management"],
        "difficulty": "Intermediate",
        "priority": "Medium",
        "description": "Predictable state container for JavaScript apps.",
        "resource": "Redux Essentials Tutorial (redux.js.org)",
        "project_idea": "Implement global shopping cart state with persistence and undo/redo.",
        "duration_weeks": 1,
    },

    # Backend Frameworks & Runtimes
    "nodejs": {
        "name": "Node.js",
        "category": "Backend Development",
        "aliases": ["node.js", "nodejs", "node"],
        "difficulty": "Intermediate",
        "priority": "High",
        "description": "JavaScript runtime built on Chrome's V8 engine for server-side apps.",
        "resource": "Nodejs.org guides & Node School (nodeschool.io)",
        "project_idea": "Build a secure RESTful API with authentication and file uploads.",
        "duration_weeks": 2,
    },
    "express": {
        "name": "Express.js",
        "category": "Backend Development",
        "aliases": ["express", "express.js", "expressjs"],
        "difficulty": "Beginner",
        "priority": "High",
        "description": "Minimalist, flexible web framework for Node.js REST APIs and routing.",
        "resource": "Expressjs.com Getting Started Guide",
        "project_idea": "Build a micro-blogging backend with JWT authentication middleware.",
        "duration_weeks": 1.5,
    },
    "flask": {
        "name": "Flask",
        "category": "Backend Development",
        "aliases": ["flask", "flask-restful"],
        "difficulty": "Beginner",
        "priority": "High",
        "description": "Lightweight, extensible Python micro-framework for web services and APIs.",
        "resource": "Flask Official Documentation & Miguel Grinberg's Flask Mega-Tutorial",
        "project_idea": "Develop a REST API with SQLite database and session management.",
        "duration_weeks": 1.5,
    },
    "django": {
        "name": "Django",
        "category": "Backend Development",
        "aliases": ["django", "django rest framework", "drf"],
        "difficulty": "Intermediate",
        "priority": "High",
        "description": "High-level Python web framework encouraging clean design and rapid development.",
        "resource": "Django Girls Tutorial & djangoproject.com Documentation",
        "project_idea": "Create a fully functional customer support ticketing portal with admin panel.",
        "duration_weeks": 2.5,
    },
    "fastapi": {
        "name": "FastAPI",
        "category": "Backend Development",
        "aliases": ["fastapi", "fast api"],
        "difficulty": "Intermediate",
        "priority": "High",
        "description": "Modern, fast Python web framework for building APIs with automatic Swagger docs.",
        "resource": "FastAPI Documentation (fastapi.tiangolo.com)",
        "project_idea": "Build an AI inference API with asynchronous request handling and schemas.",
        "duration_weeks": 1.5,
    },
    "springboot": {
        "name": "Spring Boot",
        "category": "Backend Development",
        "aliases": ["spring boot", "springboot", "spring framework", "spring"],
        "difficulty": "Advanced",
        "priority": "High",
        "description": "Enterprise Java framework for production-grade microservices and backend systems.",
        "resource": "Spring.io Guides (spring.io/guides)",
        "project_idea": "Build a banking microservice with JPA and Spring Security.",
        "duration_weeks": 3,
    },

    # Databases & Caching
    "postgresql": {
        "name": "PostgreSQL",
        "category": "Databases & Data",
        "aliases": ["postgresql", "postgres", "psql"],
        "difficulty": "Intermediate",
        "priority": "High",
        "description": "Powerful, open-source object-relational database system with strong reliability.",
        "resource": "PostgreSQL Official Tutorial & Postgres Guide",
        "project_idea": "Design an indexed relational schema with JSONB columns and triggers.",
        "duration_weeks": 2,
    },
    "mongodb": {
        "name": "MongoDB",
        "category": "Databases & Data",
        "aliases": ["mongodb", "mongo", "nosql"],
        "difficulty": "Beginner",
        "priority": "High",
        "description": "Document-based NoSQL database designed for ease of development and scaling.",
        "resource": "MongoDB University (university.mongodb.com)",
        "project_idea": "Model flexible product catalogs and aggregate analytics data.",
        "duration_weeks": 1.5,
    },
    "mysql": {
        "name": "MySQL",
        "category": "Databases & Data",
        "aliases": ["mysql", "mariadb"],
        "difficulty": "Beginner",
        "priority": "High",
        "description": "Widely deployed open-source relational database management system.",
        "resource": "MySQL Tutorial (mysqltutorial.org)",
        "project_idea": "Build database migrations and query optimization for high concurrency.",
        "duration_weeks": 1.5,
    },
    "redis": {
        "name": "Redis",
        "category": "Databases & Data",
        "aliases": ["redis", "in-memory cache", "caching"],
        "difficulty": "Intermediate",
        "priority": "Medium",
        "description": "In-memory data structure store used as a database, cache, and message broker.",
        "resource": "Redis University & Redis University CLI Tutorial",
        "project_idea": "Implement API rate limiting and session caching with expiration.",
        "duration_weeks": 1,
    },

    # Cloud, DevOps & Tools
    "docker": {
        "name": "Docker",
        "category": "Cloud & DevOps",
        "aliases": ["docker", "dockerfile", "docker-compose", "containerization"],
        "difficulty": "Intermediate",
        "priority": "High",
        "description": "Platform for containerizing applications to ensure uniform execution anywhere.",
        "resource": "Docker Getting Started Guide & Play with Docker",
        "project_idea": "Containerize a multi-container app (frontend, API, database) with docker-compose.",
        "duration_weeks": 1.5,
    },
    "kubernetes": {
        "name": "Kubernetes",
        "category": "Cloud & DevOps",
        "aliases": ["kubernetes", "k8s"],
        "difficulty": "Advanced",
        "priority": "High",
        "description": "Automated container orchestration, scaling, and management system.",
        "resource": "Kubernetes.io Tutorials & Minikube documentation",
        "project_idea": "Deploy a microservice cluster with deployments, services, and ingress configs.",
        "duration_weeks": 3,
    },
    "aws": {
        "name": "AWS (Amazon Web Services)",
        "category": "Cloud & DevOps",
        "aliases": ["aws", "amazon web services", "ec2", "s3", "lambda", "aws cloud"],
        "difficulty": "Intermediate",
        "priority": "High",
        "description": "Leading cloud platform providing compute, storage, databases, and serverless.",
        "resource": "AWS Skill Builder & Cloud Practitioner Free Learning Modules",
        "project_idea": "Deploy a serverless backend using AWS Lambda, API Gateway, and S3.",
        "duration_weeks": 3,
    },
    "azure": {
        "name": "Microsoft Azure",
        "category": "Cloud & DevOps",
        "aliases": ["azure", "microsoft azure", "azure devops"],
        "difficulty": "Intermediate",
        "priority": "Medium",
        "description": "Microsoft enterprise cloud computing services for building and scaling apps.",
        "resource": "Microsoft Learn Azure Fundamentals (AZ-900)",
        "project_idea": "Host a containerized app on Azure App Services with managed SQL database.",
        "duration_weeks": 2.5,
    },
    "gcp": {
        "name": "Google Cloud (GCP)",
        "category": "Cloud & DevOps",
        "aliases": ["gcp", "google cloud", "google cloud platform"],
        "difficulty": "Intermediate",
        "priority": "Medium",
        "description": "Cloud services platform powered by Google's infrastructure.",
        "resource": "Google Cloud Skills Boost Free Courses",
        "project_idea": "Deploy an application to Google Cloud Run with automated Cloud Build.",
        "duration_weeks": 2.5,
    },
    "git": {
        "name": "Git & GitHub",
        "category": "Development Tools",
        "aliases": ["git", "github", "gitlab", "version control"],
        "difficulty": "Beginner",
        "priority": "High",
        "description": "Distributed version control system essential for collaborative code development.",
        "resource": "Git-scm.com documentation & GitHub Skills Interactive Exercises",
        "project_idea": "Manage open-source contributions with branching, PR reviews, and rebasing.",
        "duration_weeks": 1,
    },
    "cicd": {
        "name": "CI/CD Pipelines",
        "category": "Cloud & DevOps",
        "aliases": ["ci/cd", "cicd", "continuous integration", "github actions", "jenkins"],
        "difficulty": "Intermediate",
        "priority": "High",
        "description": "Automated pipelines for testing, building, and deploying code reliably.",
        "resource": "GitHub Actions Documentation & GitLab CI Guides",
        "project_idea": "Create a workflow that runs unit tests, lints, and deploys to production on push.",
        "duration_weeks": 1.5,
    },
    "linux": {
        "name": "Linux & Bash",
        "category": "Development Tools",
        "aliases": ["linux", "bash", "shell scripting", "command line", "ubuntu"],
        "difficulty": "Beginner",
        "priority": "High",
        "description": "Standard OS environment for servers, cloud containers, and scripting.",
        "resource": "Linux Journey (linuxjourney.com)",
        "project_idea": "Write automation bash scripts for system health monitoring and backup.",
        "duration_weeks": 1,
    },

    # Architecture & Concepts
    "rest_api": {
        "name": "RESTful APIs",
        "category": "Software Architecture",
        "aliases": ["rest", "rest api", "restful", "restful api", "rest apis", "restful apis"],
        "difficulty": "Beginner",
        "priority": "High",
        "description": "Architectural standard for web APIs using standard HTTP methods and status codes.",
        "resource": "REST API Tutorial (restfulapi.net)",
        "project_idea": "Design an API with proper status codes, pagination, filtering, and error schemas.",
        "duration_weeks": 1,
    },
    "graphql": {
        "name": "GraphQL",
        "category": "Software Architecture",
        "aliases": ["graphql", "graph ql", "apollo graphql"],
        "difficulty": "Intermediate",
        "priority": "Medium",
        "description": "Query language for APIs giving clients exact control over the data they request.",
        "resource": "GraphQL.org tutorials & How to GraphQL",
        "project_idea": "Build a GraphQL server with queries, mutations, and resolvers.",
        "duration_weeks": 1.5,
    },
    "microservices": {
        "name": "Microservices Architecture",
        "category": "Software Architecture",
        "aliases": ["microservices", "microservice", "service-oriented architecture"],
        "difficulty": "Advanced",
        "priority": "Medium",
        "description": "Architectural pattern dividing systems into independently deployable services.",
        "resource": "Microservices.io & Martin Fowler Microservices Guide",
        "project_idea": "Split a monolithic application into two communicating services using message queues.",
        "duration_weeks": 2.5,
    },
    "system_design": {
        "name": "System Design",
        "category": "Software Architecture",
        "aliases": ["system design", "distributed systems", "scalability", "high availability"],
        "difficulty": "Advanced",
        "priority": "High",
        "description": "Design of large-scale, fault-tolerant, and high-performance software systems.",
        "resource": "System Design Primer (GitHub: donnemartin/system-design-primer)",
        "project_idea": "Design an end-to-end architecture diagram for a URL shortener or chat system.",
        "duration_weeks": 3,
    },
    "testing": {
        "name": "Automated Testing (Unit / Integration)",
        "category": "Quality & Testing",
        "aliases": ["unit testing", "integration testing", "pytest", "jest", "tdd", "testing", "automated testing"],
        "difficulty": "Intermediate",
        "priority": "High",
        "description": "Automated verification ensuring code correctness and preventing regressions.",
        "resource": "Testing JavaScript & Test-Driven Development Guides",
        "project_idea": "Write comprehensive unit and integration test suites with 80%+ test coverage.",
        "duration_weeks": 1.5,
    },

    # Data Science, Machine Learning & AI
    "machine_learning": {
        "name": "Machine Learning",
        "category": "Data Science & AI",
        "aliases": ["machine learning", "ml", "supervised learning", "unsupervised learning"],
        "difficulty": "Intermediate",
        "priority": "High",
        "description": "Building algorithmic models that learn patterns from data to make predictions.",
        "resource": "Andrew Ng Machine Learning Specialization (Coursera/DeepLearning.AI)",
        "project_idea": "Train predictive models for customer churn or house prices with feature engineering.",
        "duration_weeks": 3.5,
    },
    "deep_learning": {
        "name": "Deep Learning & Neural Networks",
        "category": "Data Science & AI",
        "aliases": ["deep learning", "neural networks", "cnn", "rnn", "transformers"],
        "difficulty": "Advanced",
        "priority": "High",
        "description": "Multi-layer neural networks capable of learning complex representations.",
        "resource": "Deep Learning Specialization & fast.ai Practical Deep Learning",
        "project_idea": "Train a convolutional neural network for image classification.",
        "duration_weeks": 4,
    },
    "pytorch": {
        "name": "PyTorch",
        "category": "Data Science & AI",
        "aliases": ["pytorch", "torch"],
        "difficulty": "Intermediate",
        "priority": "High",
        "description": "Premier open-source deep learning framework favored by AI research and industry.",
        "resource": "PyTorch 60-Minute Blitz (pytorch.org/tutorials)",
        "project_idea": "Implement and train a custom neural network module from scratch.",
        "duration_weeks": 2.5,
    },
    "tensorflow": {
        "name": "TensorFlow / Keras",
        "category": "Data Science & AI",
        "aliases": ["tensorflow", "keras", "tf"],
        "difficulty": "Intermediate",
        "priority": "Medium",
        "description": "End-to-end open source platform for machine learning developed by Google.",
        "resource": "TensorFlow.org tutorials",
        "project_idea": "Build and evaluate an end-to-end model pipeline with Keras.",
        "duration_weeks": 2.5,
    },
    "pandas_numpy": {
        "name": "Pandas & NumPy",
        "category": "Data Science & AI",
        "aliases": ["pandas", "numpy", "data manipulation", "data analysis"],
        "difficulty": "Beginner",
        "priority": "High",
        "description": "Essential Python scientific libraries for tabular data manipulation and numerical arrays.",
        "resource": "Pandas Official 10-Minute Guide & Kaggle Data Analysis Courses",
        "project_idea": "Perform Exploratory Data Analysis (EDA) on a real-world dataset with visual charts.",
        "duration_weeks": 1.5,
    },
    "nlp": {
        "name": "Natural Language Processing (NLP & LLMs)",
        "category": "Data Science & AI",
        "aliases": ["nlp", "natural language processing", "llm", "large language models", "langchain", "prompt engineering", "genai"],
        "difficulty": "Advanced",
        "priority": "High",
        "description": "Techniques for processing, understanding, and generating human language.",
        "resource": "Hugging Face NLP Course (huggingface.co/learn)",
        "project_idea": "Build a Retrieval-Augmented Generation (RAG) assistant over custom documents.",
        "duration_weeks": 3,
    },

    # Core Soft & Professional Skills
    "problem_solving": {
        "name": "Problem Solving & Algorithms",
        "category": "Core Competencies",
        "aliases": ["problem solving", "data structures", "algorithms", "dsa", "analytical skills"],
        "difficulty": "Intermediate",
        "priority": "High",
        "description": "Core computer science algorithms and structured troubleshooting methods.",
        "resource": "NeetCode.io & LeetCode curated patterns",
        "project_idea": "Solve 50 curated LeetCode medium questions covering trees, graphs, and dynamic programming.",
        "duration_weeks": 4,
    },
    "agile_scrum": {
        "name": "Agile & Scrum Methodologies",
        "category": "Core Competencies",
        "aliases": ["agile", "scrum", "kanban", "sprints", "jira"],
        "difficulty": "Beginner",
        "priority": "Medium",
        "description": "Iterative software development lifecycle framework prioritizing team collaboration.",
        "resource": "Scrum Guides (scrumguides.org) & Atlassian Agile Coach",
        "project_idea": "Participate in or run simulated sprint planning and retro meetings.",
        "duration_weeks": 1,
    },
    "communication": {
        "name": "Technical Communication",
        "category": "Core Competencies",
        "aliases": ["communication", "technical writing", "collaboration", "teamwork", "presentation"],
        "difficulty": "Beginner",
        "priority": "High",
        "description": "Clearly articulating technical trade-offs, architecture decisions, and code reviews.",
        "resource": "Google Technical Writing Courses (developers.google.com/tech-writing)",
        "project_idea": "Author an Architectural Decision Record (ADR) and write comprehensive README docs.",
        "duration_weeks": 1,
    },
}

# Pre-packaged sample roles for 1-click exploration
SAMPLE_ROLES = [
    {
        "id": "fullstack",
        "title": "Junior Full Stack Developer",
        "description": (
            "We are seeking an ambitious Junior Full Stack Developer to build modern web applications. "
            "Requirements:\n"
            "- Strong proficiency in JavaScript, TypeScript, and HTML/CSS\n"
            "- Hands-on experience with React and Next.js\n"
            "- Backend development using Node.js, Express, or Python/Flask\n"
            "- Solid knowledge of relational databases like PostgreSQL and SQL queries\n"
            "- Familiarity with Git version control, Docker containers, and RESTful APIs\n"
            "- Good understanding of Automated Testing and CI/CD pipelines\n"
            "- Excellent problem solving and team communication skills"
        ),
        "typical_user_skills": ["HTML & CSS", "JavaScript", "Python", "Git", "SQL"],
    },
    {
        "id": "ai_engineer",
        "title": "AI & Machine Learning Engineer",
        "description": (
            "Looking for an AI / Machine Learning Engineer to design and deploy intelligent models. "
            "Key Requirements:\n"
            "- Excellent programming skills in Python and working with Pandas & NumPy\n"
            "- Deep understanding of Machine Learning and Deep Learning architectures\n"
            "- Proficiency in PyTorch or TensorFlow for training neural networks\n"
            "- Hands-on experience with Natural Language Processing (NLP) and LLMs / RAG systems\n"
            "- Ability to deploy models using Docker and FastAPI or Flask\n"
            "- Experience using Cloud services (AWS or GCP) and Git\n"
            "- Strong background in Problem Solving & Algorithms"
        ),
        "typical_user_skills": ["Python", "Pandas & NumPy", "Machine Learning", "Git", "SQL"],
    },
    {
        "id": "devops",
        "title": "Cloud & DevOps Engineer",
        "description": (
            "Join our infrastructure team as a Cloud & DevOps Engineer. "
            "Responsibilities & Skills:\n"
            "- Strong knowledge of Linux command line and Bash scripting\n"
            "- Containerization expertise with Docker and Kubernetes (K8s)\n"
            "- Cloud infrastructure experience on AWS or Azure\n"
            "- Building robust CI/CD pipelines using GitHub Actions or GitLab\n"
            "- Scripting in Python or Go\n"
            "- Familiarity with System Design and PostgreSQL databases\n"
            "- Strong Git version control and collaborative problem-solving skills"
        ),
        "typical_user_skills": ["Linux & Bash", "Git & GitHub", "Python", "Docker"],
    },
    {
        "id": "data_scientist",
        "title": "Data Scientist / Analyst",
        "description": (
            "We are hiring a Data Scientist to extract actionable insights from big data. "
            "Requirements:\n"
            "- Expert level SQL queries, joins, and data modeling\n"
            "- High proficiency in Python and libraries like Pandas & NumPy\n"
            "- Practical Machine Learning modeling (regression, classification, clustering)\n"
            "- Knowledge of PostgreSQL or MySQL databases\n"
            "- Experience with Git version control\n"
            "- Data storytelling and strong Technical Communication\n"
            "- Familiarity with cloud platforms (AWS or GCP) is a plus"
        ),
        "typical_user_skills": ["Python", "SQL", "HTML & CSS", "Problem Solving & Algorithms"],
    },
    {
        "id": "frontend",
        "title": "Frontend React Engineer",
        "description": (
            "Looking for a creative Frontend Engineer to build responsive, accessible web interfaces. "
            "Requirements:\n"
            "- Mastery of JavaScript (ES6+), TypeScript, and HTML & CSS\n"
            "- Deep expertise in React and Next.js\n"
            "- Modern styling with Tailwind CSS\n"
            "- Experience with RESTful APIs or GraphQL integration\n"
            "- Automated testing using Jest or Cypress\n"
            "- Version control with Git & GitHub\n"
            "- Passion for UX, accessibility, and clean communication"
        ),
        "typical_user_skills": ["HTML & CSS", "JavaScript", "React", "Git & GitHub"],
    },
]


def extract_skills_from_text(text: str) -> List[Dict[str, Any]]:
    """
    Extracts recognized skills from an arbitrary text (e.g. Job Description or free-form user bio).
    Uses regex boundary matching on skill aliases to avoid false positives.
    """
    if not text:
        return []

    text_lower = text.lower()
    found_skill_keys: Set[str] = set()

    for skill_key, skill_info in SKILL_TAXONOMY.items():
        aliases = skill_info.get("aliases", [skill_info["name"].lower()])
        for alias in aliases:
            # Special regex handling for symbols like C++, C#, .NET, CI/CD, Go, R
            escaped = re.escape(alias)
            
            # Words like 'go' need strict boundary checks so we don't match 'good', 'going', etc.
            if alias in ["go", "r", "c", "ts", "js"]:
                pattern = rf"(?:\b|\s|^){escaped}(?:\b|\s|[.,;!?]|$)"
            else:
                pattern = rf"(?:\b|^){escaped}(?:\b|[.,;!?]|$)"

            if re.search(pattern, text_lower):
                found_skill_keys.add(skill_key)
                break

    # Return list of skill info dictionaries sorted by category and name
    results = [SKILL_TAXONOMY[k] for k in found_skill_keys]
    results.sort(key=lambda s: (s["category"], s["name"]))
    return results


def normalize_user_skills(skills_input: Any) -> Tuple[List[Dict[str, Any]], List[str]]:
    """
    Parses user skills from either a list of strings or comma-separated text.
    Returns:
      - recognized_skills: List of matched taxonomy skill objects
      - custom_skills: List of skills entered by user not found in taxonomy
    """
    raw_list: List[str] = []
    if isinstance(skills_input, list):
        for item in skills_input:
            if isinstance(item, str) and item.strip():
                # Might contain commas
                raw_list.extend([s.strip() for s in item.split(",") if s.strip()])
    elif isinstance(skills_input, str):
        raw_list = [s.strip() for s in skills_input.split(",") if s.strip()]

    recognized_keys: Set[str] = set()
    custom_skills: List[str] = []

    for raw_skill in raw_list:
        clean_raw = raw_skill.strip()
        if not clean_raw:
            continue

        raw_lower = clean_raw.lower()
        matched_key = None

        # Direct alias / name match
        for key, info in SKILL_TAXONOMY.items():
            if raw_lower == info["name"].lower():
                matched_key = key
                break
            if any(raw_lower == alias.lower() for alias in info.get("aliases", [])):
                matched_key = key
                break

        # Fuzzy contains check if exact match wasn't found
        if not matched_key:
            for key, info in SKILL_TAXONOMY.items():
                for alias in info.get("aliases", []):
                    if len(alias) >= 3 and alias in raw_lower:
                        matched_key = key
                        break
                if matched_key:
                    break

        if matched_key:
            recognized_keys.add(matched_key)
        else:
            # Keep user-defined custom skill
            if clean_raw.title() not in custom_skills:
                custom_skills.append(clean_raw.title())

    recognized_skills = [SKILL_TAXONOMY[k] for k in recognized_keys]
    recognized_skills.sort(key=lambda s: s["name"])
    return recognized_skills, custom_skills


def analyze_skill_gap(user_skills_input: Any, job_description: str) -> Dict[str, Any]:
    """
    Performs full skill gap analysis between user skills and job description.
    Returns comprehensive statistics, matched/missing skill lists, recommendations, and roadmap.
    """
    # 1. Parse user skills
    user_recognized, user_custom = normalize_user_skills(user_skills_input)
    user_skill_names_set = {s["name"].lower() for s in user_recognized}
    for custom in user_custom:
        user_skill_names_set.add(custom.lower())

    # 2. Extract required skills from job description
    required_skills = extract_skills_from_text(job_description)

    # If the job description is short or didn't hit our taxonomy keywords,
    # attempt fallback extraction for simple tech terms
    if not required_skills and job_description.strip():
        # Fallback: break into phrases/words
        lines = [line.strip() for line in job_description.split("\n") if line.strip()]
        for line in lines:
            line_skills = extract_skills_from_text(line)
            for ls in line_skills:
                if ls["name"] not in [r["name"] for r in required_skills]:
                    required_skills.append(ls)

    # 3. Categorize matching and missing
    matched_skills: List[Dict[str, Any]] = []
    missing_skills: List[Dict[str, Any]] = []

    for req in required_skills:
        req_name_lower = req["name"].lower()
        req_aliases = [a.lower() for a in req.get("aliases", [])]

        is_matched = False
        # Check against recognized user skills
        if req_name_lower in user_skill_names_set:
            is_matched = True
        else:
            # Check if any user custom skill matches aliases
            for u in user_skill_names_set:
                if u in req_aliases or any(alias in u for alias in req_aliases if len(alias) >= 3):
                    is_matched = True
                    break

        if is_matched:
            matched_skills.append(req)
        else:
            missing_skills.append(req)

    # 4. Identify bonus / extra skills user possesses that weren't strictly in the JD
    bonus_skills: List[Dict[str, Any]] = []
    required_names_set = {r["name"].lower() for r in required_skills}
    for u in user_recognized:
        if u["name"].lower() not in required_names_set:
            bonus_skills.append(u)

    # 5. Calculate match percentage
    total_req = len(required_skills)
    matched_count = len(matched_skills)
    missing_count = len(missing_skills)

    if total_req == 0:
        # Edge case: No explicit skills detected in JD
        match_percentage = 100 if len(user_recognized) > 0 else 0
        readiness_status = "General Review"
        readiness_badge = "neutral"
        readiness_message = "No specific technical keywords detected in this job description. Try adding specific technologies."
    else:
        # Standard match percentage formula
        raw_percentage = (matched_count / total_req) * 100
        match_percentage = round(raw_percentage)

        if match_percentage >= 80:
            readiness_status = "Job Ready! Strong Candidate"
            readiness_badge = "success"
            readiness_message = "Outstanding fit! You possess the vast majority of critical skills needed for this role. Prepare your resume and apply now."
        elif match_percentage >= 60:
            readiness_status = "Competitive Match"
            readiness_badge = "good"
            readiness_message = "You have a solid foundation with most core skills. Closing 2-3 specific gaps will make your profile top-tier."
        elif match_percentage >= 40:
            readiness_status = "Moderate Match - Targeted Upskilling Needed"
            readiness_badge = "warning"
            readiness_message = "You hold key fundamental skills. Follow the targeted learning roadmap to bridge essential framework and tooling gaps."
        else:
            readiness_status = "Foundational Stage - Structured Learning Recommended"
            readiness_badge = "danger"
            readiness_message = "This role requires several prerequisite technologies. Follow the step-by-step roadmap to build your skillset sequentially."

    # 6. Prioritize recommended skills to learn
    # High priority missing skills first, then intermediate, then others
    recommended_skills = sorted(
        missing_skills,
        key=lambda s: (
            0 if s.get("priority") == "High" else 1,
            0 if s.get("difficulty") == "Beginner" else 1 if s.get("difficulty") == "Intermediate" else 2
        )
    )

    # 7. Generate Step-by-Step Learning Roadmap
    roadmap = generate_learning_roadmap(missing_skills, matched_skills)

    # 8. Calculate total estimated roadmap learning time (weeks)
    total_estimated_weeks = sum(s.get("duration_weeks", 2) for s in missing_skills)
    estimated_time_text = (
        f"{round(total_estimated_weeks)} weeks (at 10-15 hrs/week)"
        if total_estimated_weeks > 0 else "0 weeks - Ready for interview!"
    )

    return {
        "match_percentage": match_percentage,
        "total_required": total_req,
        "matched_count": matched_count,
        "missing_count": missing_count,
        "bonus_count": len(bonus_skills) + len(user_custom),
        "readiness_status": readiness_status,
        "readiness_badge": readiness_badge,
        "readiness_message": readiness_message,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "bonus_skills": bonus_skills,
        "custom_user_skills": user_custom,
        "recommended_skills": recommended_skills,
        "roadmap": roadmap,
        "estimated_time_text": estimated_time_text,
    }


def generate_learning_roadmap(missing_skills: List[Dict[str, Any]], matched_skills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Constructs a cohesive, multi-phase chronological learning roadmap based on missing skills.
    Groups skills into logical learning phases:
      Phase 1: Core Fundamentals & Prerequisite Tools
      Phase 2: Core Technologies & Frameworks
      Phase 3: Cloud, Database & Architecture
      Phase 4: Capstone Portfolio Projects & Real-World Application
    """
    if not missing_skills:
        return [
            {
                "phase_number": 1,
                "title": "Portfolio Refinement & Interview Preparation",
                "duration": "1 - 2 Weeks",
                "focus": "Polishing existing projects, practicing technical interviews, and resume optimization.",
                "skills": [s["name"] for s in matched_skills[:5]] if matched_skills else ["Core Computer Science"],
                "action_items": [
                    "Review system design principles and standard interview algorithms.",
                    "Ensure your GitHub projects have stellar documentation, live demo links, and clean commit history.",
                    "Conduct mock behavioral and technical coding interviews.",
                    "Tailor your resume highlighting quantified achievements and your matching skill strengths."
                ],
                "capstone_project": "Deploy a showcase portfolio site featuring your best projects with live previews and case studies.",
                "resources": [
                    {"name": "Tech Interview Handbook", "url": "https://www.techinterviewhandbook.org/"},
                    {"name": "STAR Method Guide for Behavioral Interviews", "url": "https://www.themuse.com/advice/star-interview-method"}
                ]
            }
        ]

    # Partition missing skills into phases based on category & difficulty
    phase1_skills = []
    phase2_skills = []
    phase3_skills = []

    for skill in missing_skills:
        category = skill.get("category", "")
        difficulty = skill.get("difficulty", "Intermediate")

        if category in ["Programming Languages", "Development Tools", "Core Competencies"] or difficulty == "Beginner":
            phase1_skills.append(skill)
        elif category in ["Frontend Development", "Backend Development", "Databases & Data"]:
            phase2_skills.append(skill)
        else:
            # Cloud & DevOps, Software Architecture, Data Science & AI, Advanced
            phase3_skills.append(skill)

    # Rebalance if any phase is empty to keep a smooth progression
    if not phase1_skills and phase2_skills:
        phase1_skills.append(phase2_skills.pop(0))
    if not phase2_skills and phase3_skills:
        phase2_skills.append(phase3_skills.pop(0))

    roadmap_phases: List[Dict[str, Any]] = []
    phase_idx = 1

    # --- PHASE 1 ---
    if phase1_skills:
        skill_names = [s["name"] for s in phase1_skills]
        p1_weeks = round(sum(s.get("duration_weeks", 1.5) for s in phase1_skills))
        p1_resources = [{"name": s["name"] + " Tutorial", "info": s["resource"]} for s in phase1_skills[:3]]
        roadmap_phases.append({
            "phase_number": phase_idx,
            "title": "Phase 1: Foundations & Core Tooling",
            "duration": f"Weeks 1 - {max(2, p1_weeks)}",
            "focus": f"Master syntax, basic concepts, and workflows for: {', '.join(skill_names)}.",
            "skills": skill_names,
            "action_items": [
                f"Complete interactive starter modules for {s['name']}: {s['resource']}" for s in phase1_skills[:3]
            ] + [
                "Set up local development environment, Git version control, and write daily code snippets.",
                "Implement 2-3 mini exercises to solidify foundational syntax and error troubleshooting."
            ],
            "capstone_project": phase1_skills[0].get("project_idea", "Build a structured starter application demonstrating basic concepts."),
            "resources": p1_resources
        })
        phase_idx += 1

    # --- PHASE 2 ---
    if phase2_skills:
        skill_names = [s["name"] for s in phase2_skills]
        p2_weeks = round(sum(s.get("duration_weeks", 2) for s in phase2_skills))
        p2_resources = [{"name": s["name"] + " Official Docs", "info": s["resource"]} for s in phase2_skills[:3]]
        roadmap_phases.append({
            "phase_number": phase_idx,
            "title": f"Phase {phase_idx}: Modern Frameworks & Application Architecture",
            "duration": f"{p2_weeks} Weeks",
            "focus": f"Build robust, production-style functionality using: {', '.join(skill_names)}.",
            "skills": skill_names,
            "action_items": [
                f"Learn idiomatic patterns and best practices for {s['name']}." for s in phase2_skills[:3]
            ] + [
                "Implement secure data validation, error handling middleware, and clean modular code architecture.",
                "Connect frontend interfaces with backend services and database persistent storage."
            ],
            "capstone_project": phase2_skills[0].get("project_idea", "Develop a full-featured CRUD web application with authenticated routes."),
            "resources": p2_resources
        })
        phase_idx += 1

    # --- PHASE 3 ---
    if phase3_skills:
        skill_names = [s["name"] for s in phase3_skills]
        p3_weeks = round(sum(s.get("duration_weeks", 2.5) for s in phase3_skills))
        p3_resources = [{"name": s["name"] + " Guide", "info": s["resource"]} for s in phase3_skills[:3]]
        roadmap_phases.append({
            "phase_number": phase_idx,
            "title": f"Phase {phase_idx}: Cloud, DevOps & Scalability",
            "duration": f"{p3_weeks} Weeks",
            "focus": f"Production deployment, testing, and system reliability for: {', '.join(skill_names)}.",
            "skills": skill_names,
            "action_items": [
                f"Study real-world deployment patterns and orchestration for {s['name']}." for s in phase3_skills[:3]
            ] + [
                "Set up automated CI/CD pipeline triggers on GitHub pull requests.",
                "Perform load testing, log monitoring, and containerized deployment."
            ],
            "capstone_project": phase3_skills[0].get("project_idea", "Deploy a containerized production service with automated testing and continuous deployment."),
            "resources": p3_resources
        })
        phase_idx += 1

    # --- FINAL CAPSTONE & INTERVIEW PHASE ---
    all_missing_names = [s["name"] for s in missing_skills]
    roadmap_phases.append({
        "phase_number": phase_idx,
        "title": f"Phase {phase_idx}: Capstone Portfolio & Job Application Readiness",
        "duration": "2 Weeks",
        "focus": "Tie all newly mastered skills into a cohesive, standout portfolio project.",
        "skills": all_missing_names[:6],
        "action_items": [
            "Build an end-to-end Capstone project incorporating both your existing strengths and new skills.",
            "Record a 2-minute video walkthrough showcasing your architecture decisions and live demo.",
            "Update your LinkedIn and resume highlighting quantifiable achievements with the newly acquired skills.",
            "Practice technical interview questions related to the core tools in this roadmap."
        ],
        "capstone_project": (
            f"Comprehensive Capstone: Build an end-to-end application integrating "
            f"{all_missing_names[0] if all_missing_names else 'full stack'} with clean documentation and live deployment."
        ),
        "resources": [
            {"name": "GitHub Profile Readme Best Practices", "info": "https://docs.github.com/en/account-and-profile"},
            {"name": "System Design Primer & Tech Guides", "info": "https://github.com/donnemartin/system-design-primer"}
        ]
    })

    return roadmap_phases


def get_popular_skills() -> List[str]:
    """Returns a curated list of top skills for quick-add pill tags."""
    return [
        "Python", "JavaScript", "TypeScript", "React", "Next.js",
        "Node.js", "Flask", "Django", "SQL", "PostgreSQL",
        "MongoDB", "Docker", "AWS", "Git & GitHub", "HTML & CSS",
        "Tailwind CSS", "Linux & Bash", "Machine Learning", "RESTful APIs",
        "Problem Solving & Algorithms"
    ]
