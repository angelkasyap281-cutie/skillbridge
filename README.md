# 🚀 SkillBridge AI

> **Bridge the gap between your current skills and your dream job.**  
> An intelligent, modern career readiness web application built with Python, Flask, HTML, CSS, and JavaScript.

![SkillBridge AI](https://img.shields.io/badge/Status-Complete-emerald?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-black?style=for-the-badge&logo=flask)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

---

## 🌟 Key Features

1. **🎨 Ultra-Modern, Responsive UI**:
   - Sleek dark theme with ambient glowing accents, glassmorphic cards, and clean typography (*Inter* & *Outfit*).
   - Fully responsive across mobile smartphones, tablets, and desktop displays.

2. **🏷️ Interactive Skill Tag Input**:
   - Type any skill and hit <kbd>Enter</kbd> or comma (`,`) to add interactive chips.
   - Quick-add common tech skills with 1-click suggestion pills.
   - Remove chips individually with `×` or clear all in one go.

3. **📄 Job Description Analyzer**:
   - Paste any real job posting from LinkedIn, Indeed, or company career sites.
   - One-click sample role loader (*Junior Full Stack Developer, AI & ML Engineer, Cloud & DevOps, Data Scientist, Frontend Engineer*).

4. **⚡ Instant Skill Gap Analysis**:
   - **Match Score Percentage**: Animated circular progress gauge displaying your alignment score.
   - **Job Readiness Assessment**: Automatic classification (*Job Ready, Strong Candidate, Moderate Match, or Foundational Stage*).
   - **Matched Skills**: Highlights the skills you already possess that satisfy the job listing.
   - **Missing Skills**: Pinpoints critical technology gaps prioritized by industry demand.
   - **Bonus Skills**: Showcases additional skills you have that give you an extra competitive edge.

5. **🗺️ Step-by-Step Personalized Learning Roadmap**:
   - 4 chronological learning phases (Foundations, Core Stack, DevOps & Architecture, Capstone).
   - Realistic time estimates (e.g. `Weeks 1-3`).
   - Hands-on Capstone mini-project ideas to build portfolio evidence.
   - Curated free documentation and tutorial resources.

6. **🖨️ Export & Utilities**:
   - **Print / Save Roadmap**: Formats an executive PDF-ready summary using print stylesheets.
   - **Copy Summary**: 1-click clipboard export for personal tracking or notes.

7. **🔒 100% Offline & Free**:
   - Works immediately out-of-the-box with built-in knowledge bases without requiring external API keys.

---

## 📁 Project Structure

```
skillbridge/
├── app.py                 # Flask server & REST API endpoints
├── analyzer.py            # Skill taxonomy engine, regex extraction, gap calculations & roadmap builder
├── requirements.txt       # Project dependencies (Flask)
├── README.md              # Documentation & setup guide
├── templates/
│   └── index.html         # Modern semantic HTML5 layout & dashboard
└── static/
    ├── css/
    │   └── style.css      # Glassmorphism design system & responsive stylesheet
    └── js/
        └── app.js         # Interactive tag chips, API client, animated progress ring & roadmap UI
```

---

## 🚀 How to Start the Application

### 1. Prerequisites
Make sure **Python** is installed on your computer. You can check by running:
```bash
python --version
```

### 2. Install Dependencies
Open your terminal in the project folder (`c:\skillbridge`) and run:
```bash
pip install -r requirements.txt
```

### 3. Run the Flask Server
Start the application with:
```bash
python app.py
```

### 4. Open in Your Browser
Once running, open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 💡 How to Use

1. **Enter Your Current Skills**: Type your skills into the top-left box (e.g., `Python`, `SQL`, `Git`) or click the popular skill pills below.
2. **Add a Job Description**: Either paste text from a job posting into the right box, or click one of the pre-loaded **Sample Roles** at the top.
3. **Click "Analyze Skills & Generate Roadmap"**: The engine will calculate your percentage match, display missing skills, and build your custom roadmap!
4. **Follow the Roadmap**: Work through the phases, complete the suggested projects, and prepare for interviews.

---

## 🛠️ Technology Stack

- **Backend**: Python 3, Flask
- **Frontend**: Semantic HTML5, CSS3 (Vanilla Glassmorphism Design System), Modern Vanilla JavaScript (ES6+)
- **Icons & Fonts**: FontAwesome 6, Google Fonts (Outfit & Inter)
