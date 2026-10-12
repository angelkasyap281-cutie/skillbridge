"""
app.py - SkillBridge AI Flask Application
Main web server providing REST endpoints and serving the modern web application.
"""

from flask import Flask, render_template, request, jsonify
from analyzer import (
    analyze_skill_gap,
    SAMPLE_ROLES,
    get_popular_skills,
    SKILL_TAXONOMY,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "skillbridge-ai-secret-key-2026"


@app.route("/")
def index():
    """Serves the main SkillBridge AI landing page and dashboard."""
    popular_skills = get_popular_skills()
    return render_template(
        "index.html",
        sample_roles=SAMPLE_ROLES,
        popular_skills=popular_skills,
        total_skills_catalog=len(SKILL_TAXONOMY),
    )


@app.route("/api/analyze", methods=["POST"])
def analyze_skills():
    """
    Analyzes user skills against a target job description.
    Expected JSON body:
      {
        "user_skills": ["Python", "JavaScript", ...],
        "job_description": "We are seeking a developer with skills in..."
      }
    """
    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({
                "success": False,
                "error": "Invalid request. Please provide JSON payload."
            }), 400

        user_skills = data.get("user_skills", [])
        job_description = data.get("job_description", "").strip()

        if not job_description:
            return jsonify({
                "success": False,
                "error": "Please provide a target job description to analyze."
            }), 400

        # Perform comprehensive gap analysis and roadmap generation
        results = analyze_skill_gap(user_skills, job_description)

        return jsonify({
            "success": True,
            "data": results
        })

    except Exception as e:
        app.logger.error(f"Error during analysis: {e}")
        return jsonify({
            "success": False,
            "error": f"An error occurred while analyzing skills: {str(e)}"
        }), 500


@app.route("/api/presets", methods=["GET"])
def get_presets():
    """Returns sample job role templates."""
    return jsonify({
        "success": True,
        "roles": SAMPLE_ROLES
    })


@app.route("/api/popular-skills", methods=["GET"])
def get_skills_list():
    """Returns list of curated top skills for quick-tag pills."""
    return jsonify({
        "success": True,
        "skills": get_popular_skills()
    })


@app.errorhandler(404)
def not_found(e):
    return render_template(
        "index.html",
        sample_roles=SAMPLE_ROLES,
        popular_skills=get_popular_skills(),
        total_skills_catalog=len(SKILL_TAXONOMY),
    ), 404


if __name__ == "__main__":
    # Run development server on port 5000
    print("=" * 60)
    print(" SkillBridge AI is running!")
    print(" Open your browser and visit: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=True)
