import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, Preformatted, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf():
    pdf_filename = "SCSE3040_P06_S24CSEU2521.pdf"
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=32,
        bottomMargin=32
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=3
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569'),
        spaceAfter=10
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=8,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#1e293b')
    )

    body_small = ParagraphStyle(
        'BodySmall',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#334155')
    )

    body_small_bold = ParagraphStyle(
        'BodySmallBold',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#0f172a')
    )

    link_style = ParagraphStyle(
        'LinkStyle',
        parent=body_style,
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#0969da')
    )

    story = []

    # Title Banner
    story.append(Paragraph("SCSE3040 — Machine Learning Operations", title_style))
    story.append(Paragraph("Practical 06: Remembering Every Experiment &middot; Tracking, Comparing &amp; Registry Submission", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563eb'), spaceBefore=0, spaceAfter=8))

    # 1. Student Details Table
    story.append(Paragraph("1. Student & Laboratory Session Information", section_heading))
    student_data = [
        [Paragraph("<b>Student Name:</b>", body_style), Paragraph("Vishesh Aggarwal", body_style),
         Paragraph("<b>Roll Number:</b>", body_style), Paragraph("S24CSEU2521", body_style)],
        [Paragraph("<b>Batch:</b>", body_style), Paragraph("Batch 2024–2028 (Session 2026–27)", body_style),
         Paragraph("<b>Date of Session:</b>", body_style), Paragraph("4 October 2026", body_style)]
    ]
    t_student = Table(student_data, colWidths=[95, 165, 95, 168])
    t_student.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_student)
    story.append(Spacer(1, 8))

    # 2. Repository Link
    story.append(Paragraph("2. Repository Link", section_heading))
    repo_url = "https://github.com/visheshaggarwal0/MLOps_Lab"
    repo_text = f'<a href="{repo_url}"><font color="#0969da"><u>{repo_url}</u></font></a>'
    repo_box = Table([[Paragraph(repo_text, link_style)]], colWidths=[523])
    repo_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(repo_box)
    story.append(Spacer(1, 8))

    # 3. Screenshot of MLflow UI Runs Table
    story.append(Paragraph("3. MLflow UI Runs Table (Experiment: <code>delivery-time</code>)", section_heading))
    
    # Insert cropped runs table screenshot
    img_runs_path = "crop_runs_table.png"
    img_w = 523
    img_h = img_w * (847 / 1918) # scaled ratio
    img_runs_flowable = Image(img_runs_path, width=img_w, height=img_h)
    
    img_runs_table_box = Table([[img_runs_flowable]], colWidths=[523])
    img_runs_table_box.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 1),
        ('RIGHTPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(img_runs_table_box)
    story.append(Spacer(1, 6))

    # Side-by-side run parameter & metric comparison table
    runs_comparison_data = [
        [Paragraph("<b>Run Name</b>", body_small_bold), 
         Paragraph("<b>Model Architecture</b>", body_small_bold),
         Paragraph("<b>n_estimators</b>", body_small_bold), 
         Paragraph("<b>max_depth</b>", body_small_bold), 
         Paragraph("<b>MAE (min)</b>", body_small_bold),
         Paragraph("<b>RMSE (min)</b>", body_small_bold),
         Paragraph("<b>Registry Status</b>", body_small_bold)],
        [Paragraph("<b>champion</b>", body_small_bold), Paragraph("RandomForestRegressor", body_small), Paragraph("300", body_small), Paragraph("12", body_small), Paragraph("<b>2.3770</b>", body_small_bold), Paragraph("3.0795", body_small), Paragraph("Registered: <code>v1</code>", body_small)],
        [Paragraph("rf-n300-d12", body_small), Paragraph("RandomForestRegressor", body_small), Paragraph("300", body_small), Paragraph("12", body_small), Paragraph("2.3770", body_small), Paragraph("3.0795", body_small), Paragraph("Optimal Sweep Run", body_small)],
        [Paragraph("rf-n200-dNone", body_small), Paragraph("RandomForestRegressor", body_small), Paragraph("200", body_small), Paragraph("None (Unlimited)", body_small), Paragraph("2.4117", body_small), Paragraph("3.1050", body_small), Paragraph("Tracked", body_small)],
        [Paragraph("rf-n150-d8", body_small), Paragraph("RandomForestRegressor", body_small), Paragraph("150", body_small), Paragraph("8", body_small), Paragraph("2.4262", body_small), Paragraph("3.0904", body_small), Paragraph("Tracked", body_small)],
        [Paragraph("rf-n100-d6", body_small), Paragraph("RandomForestRegressor", body_small), Paragraph("100", body_small), Paragraph("6", body_small), Paragraph("2.6144", body_small), Paragraph("3.3093", body_small), Paragraph("Tracked", body_small)],
        [Paragraph("rf-n50-d4", body_small), Paragraph("RandomForestRegressor", body_small), Paragraph("50", body_small), Paragraph("4", body_small), Paragraph("3.5288", body_small), Paragraph("4.3126", body_small), Paragraph("Tracked", body_small)],
    ]
    t_comp = Table(runs_comparison_data, colWidths=[80, 115, 68, 80, 60, 60, 60])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#ecfdf5')), # highlight winner
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (2,0), (5,-1), 'CENTER'),
    ]))
    story.append(t_comp)

    # Page 2: Run Detail Page, Selection details & AI disclosure
    story.append(PageBreak())

    # 4. Screenshot of the Run Detail Page
    story.append(Paragraph("4. Run &amp; Model Detail Verification (Winning Run: <code>champion</code>)", section_heading))
    
    img_best_path = "crop_best_run.png"
    img_hb = img_w * (851 / 1918)
    img_best_flowable = Image(img_best_path, width=img_w, height=img_hb)
    
    img_best_box = Table([[img_best_flowable]], colWidths=[523])
    img_best_box.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 1),
        ('RIGHTPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(img_best_box)
    story.append(Spacer(1, 12))

    # 5. Selected Run Information & Justification
    story.append(Paragraph("5. Best Run Selection Details &amp; Evaluation", section_heading))
    
    best_run_data = [
        [Paragraph("<b>Selected Run Name:</b>", body_style), Paragraph("<code>champion</code> (retrained from sweep winner <code>rf-n300-d12</code>)", body_style)],
        [Paragraph("<b>Run ID:</b>", body_style), Paragraph("<code>23d4b67fc9c0443397da7196238ddf96</code>", body_style)],
        [Paragraph("<b>Primary Metric:</b>", body_style), Paragraph("<b>MAE = 2.377006 minutes</b> &nbsp;|&nbsp; RMSE = 3.079530 minutes", body_style)],
        [Paragraph("<b>Optimal Parameters:</b>", body_style), Paragraph("<code>n_estimators: 300</code>, &nbsp; <code>max_depth: 12</code>", body_style)],
        [Paragraph("<b>Registered Version:</b>", body_style), Paragraph("Registered to Model Registry as <b><code>delivery-time-model</code> Version 1</b>", body_style)],
        [Paragraph("<b>Selection Rationale:</b>", body_style), Paragraph(
            "I chose the <code>champion</code> run because it achieved the lowest Mean Absolute Error "
            "(<b>2.377 minutes</b>) across all evaluated non-linear ensemble models—outperforming the shallow "
            "baseline by over <b>1.15 minutes</b>—while maintaining controlled tree depth to avoid unconstrained overfitting, "
            "making it the optimal production model packaged with input schema artifacts in the MLflow Model Registry.",
            body_style
        )]
    ]
    t_best = Table(best_run_data, colWidths=[130, 393])
    t_best.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_best)
    story.append(Spacer(1, 12))

    # 6. AI Use Disclosure
    story.append(Paragraph("6. AI Use Disclosure", section_heading))
    ai_text = (
        "<b>Antigravity (powered by Gemini Flash)</b> was utilized to assist in formatting the laboratory "
        "submission report, organizing the experimental tracking data, and preparing the visual artifacts "
        "in accordance with the SCSE3040 course academic integrity policy."
    )
    ai_box = Table([[Paragraph(ai_text, body_style)]], colWidths=[523])
    ai_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(ai_box)

    def add_header_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 8.5)
        canvas.setFillColor(colors.HexColor('#64748b'))
        # Footer
        canvas.drawString(36, 18, "SCSE3040: Machine Learning Operations — Practical 06 Lab Submission")
        canvas.drawRightString(559, 18, f"Roll No: S24CSEU2521  |  Page {doc.page} of 2")
        canvas.restoreState()

    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    file_size_mb = os.path.getsize(pdf_filename) / (1024 * 1024)
    print(f"Successfully generated {pdf_filename} ({file_size_mb:.2f} MB)")

if __name__ == "__main__":
    generate_pdf()
