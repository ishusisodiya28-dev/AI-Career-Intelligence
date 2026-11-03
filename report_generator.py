
from pathlib import Path
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def safe_text(value):
    if value is None:
        return "Not available"

    text = str(value)

    # Built-in ReportLab fonts support Latin-1 text.
    text = text.encode(
        "latin-1",
        errors="replace"
    ).decode("latin-1")

    return escape(text).replace("\n", "<br/>")


def generate_pdf_report(report_data, output_path):

    output_path = Path(output_path)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=21,
        leading=26,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#183153"),
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name="SectionTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=colors.HexColor("#183153"),
        spaceBefore=13,
        spaceAfter=7
    ))

    styles.add(ParagraphStyle(
        name="ReportBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=14,
        spaceAfter=5
    ))

    styles.add(ParagraphStyle(
        name="SmallText",
        parent=styles["BodyText"],
        fontSize=8,
        leading=11
    ))

    styles.add(ParagraphStyle(
        name="TableHeader",
        fontName="Helvetica-Bold",
        fontSize=8,
        textColor=colors.white
    ))

    story = []

    def paragraph(value, style="ReportBody"):
        return Paragraph(
            safe_text(value),
            styles[style]
        )

    def add_heading(title):
        story.append(
            paragraph(title, "SectionTitle")
        )

    def add_bullets(title, items):

        add_heading(title)

        if not items:
            story.append(
                paragraph("No information detected.")
            )
            return

        for item in items:
            story.append(
                paragraph("&#8226; " + str(item))
            )

    def add_table(headers, rows, widths=None):

        table_data = [[
            paragraph(item, "TableHeader")
            for item in headers
        ]]

        for row in rows:
            table_data.append([
                paragraph(item, "SmallText")
                for item in row
            ])

        table = Table(
            table_data,
            colWidths=widths,
            repeatRows=1
        )

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0),
             colors.HexColor("#183153")),
            ("GRID", (0, 0), (-1, -1), 0.4,
             colors.HexColor("#D5DDE5")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7)
        ]))

        story.append(table)
        story.append(Spacer(1, 8))

    # Title
    story.append(
        paragraph(
            "AI CAREER INTELLIGENCE",
            "ReportTitle"
        )
    )

    story.append(
        paragraph(
            "Resume Analysis and Career Recommendation Report",
            "ReportBody"
        )
    )

    story.append(
        paragraph(
            "Generated on: " + datetime.now().strftime("%d %B %Y"),
            "SmallText"
        )
    )

    story.append(Spacer(1, 12))

    # Candidate details
    candidate = report_data["candidate"]

    add_heading("1. Candidate Profile")

    add_table(
        ["Field", "Details"],
        [
            ["Name", candidate.get("name") or "Not detected"],
            ["Email", candidate.get("email") or "Not detected"],
            ["Phone", candidate.get("phone") or "Not detected"],
            ["Resume ID", report_data["resume_id"]],
            ["Target Job", report_data["job_title"]],
            ["Career Role", report_data["target_role"]]
        ],
        [45 * mm, 115 * mm]
    )

    # Education and skills
    add_bullets(
        "2. Education",
        report_data["education"]
    )

    add_bullets(
        "3. Technical Skills",
        report_data["technical_skills"]
    )

    add_bullets(
        "4. Projects",
        report_data["projects"]
    )

    add_bullets(
        "5. Experience",
        report_data["experience"]
    )

    add_bullets(
        "6. Certifications",
        report_data["certifications"]
    )

    # Job matching
    match = report_data["matching_results"]

    add_heading("7. AI Job Matching Analysis")

    add_table(
        ["Metric", "Result"],
        [
            [
                "Overall Match Score",
                str(match["overall_match_score"]) + "%"
            ],
            [
                "Skill Match Score",
                str(match["skill_match_score"])
                + "%"
                if match["skill_match_score"] is not None
                else "Not available"
            ],
            [
                "Text Similarity Score",
                str(match["text_similarity_score"]) + "%"
            ]
        ],
        [75 * mm, 85 * mm]
    )

    add_bullets(
        "Matched Skills",
        match["matched_skills"]
    )

    add_bullets(
        "Missing Skills",
        match["missing_skills"]
    )

    # ATS Analysis
    ats = report_data["ats_analysis"]

    add_heading("8. ATS Compatibility Analysis")

    add_table(
        ["Metric", "Result"],
        [
            [
                "ATS Readiness Estimate",
                str(ats["ats_compatibility_score"]) + "%"
            ],
            [
                "Resume Word Count",
                ats["word_count"]
            ],
            [
                "Keyword Match",
                str(ats["keyword_match_percentage"])
                + "%"
                if ats["keyword_match_percentage"] is not None
                else "Not available"
            ]
        ],
        [75 * mm, 85 * mm]
    )

    # ATS suggestions
    add_bullets(
        "ATS Improvement Suggestions",
        ats["suggestions"]
    )

    # Career Recommendations
    add_heading("9. Career Recommendations")

    recommendation_rows = []

    for item in report_data["career_recommendations"]:

        recommendation_rows.append([
            item["job_role"],
            str(item["match_score"]) + "%",
            ", ".join(item["matched_skills"]) or "None"
        ])

    if recommendation_rows:

        add_table(
            ["Job Role", "Match", "Matched Skills"],
            recommendation_rows,
            [55 * mm, 25 * mm, 80 * mm]
        )

    else:
        story.append(
            paragraph("No recommendations available.")
        )

    # Learning roadmap
    roadmap = report_data["learning_roadmap"]

    add_heading("10. Personalized Learning Roadmap")

    story.append(
        paragraph(
            "Selected Career Role: " + roadmap["job_role"]
        )
    )

    story.append(
        paragraph(
            "Estimated Duration: "
            + str(roadmap["estimated_duration_weeks"])
            + " weeks"
        )
    )

    for week in roadmap["weekly_learning_roadmap"]:

        story.append(
            paragraph(
                "Week "
                + str(week["week"])
                + ": "
                + week["skill_to_learn"],
                "SectionTitle"
            )
        )

        story.append(
            paragraph(
                "Topics: "
                + ", ".join(week["learning_topics"])
            )
        )

        story.append(
            paragraph(
                "Practice: "
                + week["practice_task"]
            )
        )

        story.append(
            paragraph(
                "Resource: "
                + week["recommended_resource"]
            )
        )

    story.append(
        paragraph(
            "Final Project: "
            + roadmap["final_capstone_project"]
        )
    )

    # Interview questions
    interview = report_data["interview"]

    add_heading("11. Interview Preparation")

    all_questions = (
        interview["technical_questions"]
        + interview["project_questions"]
        + interview["behavioral_questions"]
    )

    for index, question in enumerate(all_questions, start=1):

        story.append(
            paragraph(
                f"{index}. [{question['category']}] "
                + question["question"]
            )
        )

        story.append(
            paragraph(
                "Sample Answer: "
                + question["sample_answer"],
                "SmallText"
            )
        )

        story.append(Spacer(1, 5))

    # Disclaimer
    add_heading("12. Important Note")

    story.append(
        paragraph(
            "This report contains automated, rule-based "
            "resume analysis and learning recommendations. "
            "Matching and ATS scores are estimates, not "
            "official hiring decisions or guarantees. "
            "Review all extracted information for accuracy."
        )
    )

    def add_footer(canvas, doc):

        canvas.saveState()

        canvas.setFont("Helvetica", 8)

        canvas.setFillColor(
            colors.HexColor("#666666")
        )

        canvas.drawString(
            18 * mm,
            12 * mm,
            "AI Career Intelligence"
        )

        canvas.drawRightString(
            A4[0] - 18 * mm,
            12 * mm,
            f"Page {doc.page}"
        )

        canvas.restoreState()

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=20 * mm,
        title="AI Career Intelligence Report"
    )

    doc.build(
        story,
        onFirstPage=add_footer,
        onLaterPages=add_footer
    )

    return output_path
