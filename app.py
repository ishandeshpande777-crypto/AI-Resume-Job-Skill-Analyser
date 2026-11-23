from flask import send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

from flask import Flask, render_template, request
from pypdf import PdfReader
from analyzer import (
    extract_skills,
    analyze_skills,
    recommend_skills,
    calculate_text_similarity,
    check_resume_sections,
    calculate_resume_quality
)

app = Flask(__name__)

# Maximum upload size: 5 MB
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    resume = request.files.get("resume")
    job_description = request.form.get("job_description", "")

    if not resume or resume.filename == "":
        return render_template(
            "index.html",
            error="Please select a resume."
        )

    if not resume.filename.lower().endswith(".pdf"):
        return render_template(
            "index.html",
            error="Please upload a PDF file only."
        )

    if not job_description.strip():
        return render_template(
            "index.html",
            error="Please enter a job description."
        )

    try:
        reader = PdfReader(resume.stream)

        if reader.is_encrypted:
            return render_template(
                "index.html",
                error="Please upload an unlocked PDF."
            )

        resume_text = ""

        for page in reader.pages:
            resume_text += page.extract_text() or ""

        if not resume_text.strip():
            return render_template(
                "index.html",
                error="No readable text found. Please use a text-based PDF."
            )

        # Extract skills
        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)

        if not job_skills:
            return render_template(
                "index.html",
                error="No recognized skills found in the job description. Add skills such as Python, SQL or Java."
            )

        # Compare skills
        matched, missing, score = analyze_skills(
            resume_skills,
            job_skills
        )

        # Calculate AI text similarity
        ai_similarity = calculate_text_similarity(
            resume_text,
            job_description
        )

        resume_sections = check_resume_sections(resume_text)

        resume_quality, quality_suggestions = calculate_resume_quality(
            resume_text,
            resume_skills,
            resume_sections
        )

        # Generate recommendations
        recommendations = recommend_skills(missing)

        return render_template(
            "result.html",
            matched=matched,
            missing=missing,
            score=score,
            recommendations=recommendations,
            resume_skills=resume_skills,
            ai_similarity=ai_similarity,
            resume_sections=resume_sections,
            resume_quality=resume_quality,
            quality_suggestions=quality_suggestions
        )

    except Exception:
        return render_template(
            "index.html",
            error="Unable to read this PDF. Please try another file."
        )


@app.errorhandler(413)
def file_too_large(error):
    return render_template(
        "index.html",
        error="File is too large. Maximum size is 5 MB."
    ), 413


if __name__ == "__main__":
    app.run(debug=True)

@app.route("/download-report", methods=["POST"])
def download_report():

    from flask import request

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4

    y = height - 50

    # Title
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50, y, "AI Resume Job Skill Analyser")

    y -= 35

    pdf.setFont("Helvetica", 10)
    pdf.drawString(
        50, y,
        "Analysis Report: " + datetime.now().strftime("%d-%m-%Y")
    )

    y -= 40

    # Analysis scores
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Analysis Results")

    y -= 25

    pdf.setFont("Helvetica", 11)

    pdf.drawString(
        50, y,
        "Skill Match Score: " + request.form.get("score", "0") + "%"
    )

    y -= 20

    pdf.drawString(
        50, y,
        "Text Similarity: " + request.form.get("ai_similarity", "0") + "%"
    )

    y -= 20

    pdf.drawString(
        50, y,
        "Resume Quality: " + request.form.get("quality_score", "0") + "%"
    )

    y -= 35

    # Matched skills
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Matched Skills")

    y -= 22

    pdf.setFont("Helvetica", 10)

    matched = request.form.get("matched", "")
    pdf.drawString(50, y, matched[:100] or "None")

    y -= 35

    # Missing skills
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Missing Skills")

    y -= 22

    pdf.setFont("Helvetica", 10)

    missing = request.form.get("missing", "")
    pdf.drawString(50, y, missing[:100] or "None")

    y -= 35

    # Footer
    pdf.setFont("Helvetica-Oblique", 9)
    pdf.drawString(
        50, y,
        "Generated by AI Resume Job Skill Analyser"
    )

    pdf.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Resume_Analysis_Report.pdf",
        mimetype="application/pdf"
    )