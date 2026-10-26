import os
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, Preformatted, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Update screenshot if needed
from generate_terminal_screenshot import create_terminal_screenshot

def generate_pdf():
    pdf_filename = "SCSE3040_P05_S24CSEU2521.pdf"
    screenshot_path = "terminal_pytest.png"
    
    # Ensure screenshot exists
    create_terminal_screenshot(screenshot_path)
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f172a'),
        alignment=0,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569'),
        spaceAfter=12
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#1e293b')
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Times-Bold'
    )

    link_style = ParagraphStyle(
        'LinkStyle',
        parent=body_style,
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#0969da')
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1e293b')
    )

    story = []

    # Title Banner
    story.append(Paragraph("SCSE3040 — Machine Learning Operations", title_style))
    story.append(Paragraph("Practical 05: Settings in a File, Bugs Caught by a Robot &middot; Lab Submission Record", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563eb'), spaceBefore=0, spaceAfter=10))

    # 1. Student Details Table
    story.append(Paragraph("1. Student & Laboratory Session Information", section_heading))
    
    student_data = [
        [Paragraph("<b>Student Name:</b>", body_style), Paragraph("Vishesh Aggarwal", body_style),
         Paragraph("<b>Roll Number:</b>", body_style), Paragraph("S24CSEU2521", body_style)],
        [Paragraph("<b>Batch:</b>", body_style), Paragraph("Batch 2024–2028 (Session 2026–27)", body_style),
         Paragraph("<b>Date of Session:</b>", body_style), Paragraph("4 October 2026", body_style)]
    ]
    
    t_student = Table(student_data, colWidths=[100, 160, 95, 160])
    t_student.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_student)
    story.append(Spacer(1, 10))

    # 2. Repository Link
    story.append(Paragraph("2. Repository Link", section_heading))
    repo_url = "https://github.com/visheshaggarwal0/MLOps_Lab"
    repo_text = f'<a href="{repo_url}"><font color="#0969da"><u>{repo_url}</u></font></a>'
    
    repo_box = Table([[Paragraph(repo_text, link_style)]], colWidths=[515])
    repo_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(repo_box)
    story.append(Spacer(1, 10))

    # 3. Contents of config.yaml
    story.append(Paragraph("3. Contents of config.yaml", section_heading))
    config_path = Path("work") / "config.yaml"
    config_content = config_path.read_text(encoding="utf-8")
    
    config_table = Table([[Preformatted(config_content.strip(), code_style)]], colWidths=[515])
    config_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(config_table)
    
    # Clean page break so Section 4, 5, 6 are grouped elegantly on Page 2
    from reportlab.platypus import PageBreak
    story.append(PageBreak())

    # 4. Terminal Screenshot of pytest
    story.append(Paragraph("4. Terminal Verification — pytest Test Suite Output", section_heading))
    
    # High-quality prominent display on Page 2
    img_w = 515
    img_h = img_w * (580 / 1100) # approximately based on generated image height
    img_flowable = Image(screenshot_path, width=img_w, height=img_h)
    
    img_table = Table([[img_flowable]], colWidths=[515])
    img_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 1),
        ('RIGHTPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(img_table)
    story.append(Spacer(1, 14))

    # 5. Number produced before and after refactor
    story.append(Paragraph("5. Model Output Comparison (Before vs. After Refactor)", section_heading))
    metric_text = (
        "<b>Before the refactor</b>, the baseline pipeline produced an MAE of <b>1.92 minutes</b>; "
        "<b>after refactoring</b> to use <code>config.yaml</code>, it produces an MAE of <b>1.92 minutes</b> "
        "(and <b>2.18 minutes</b> when constrained to the first 300 orders via the Task T1 <code>max_rows: 300</code> setting)."
    )
    metric_box = Table([[Paragraph(metric_text, body_style)]], colWidths=[515])
    metric_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(metric_box)
    story.append(Spacer(1, 14))

    # 6. AI Use Disclosure
    story.append(Paragraph("6. AI Use Disclosure", section_heading))
    ai_text = (
        "<b>Antigravity (powered by Gemini Flash)</b> was utilized to assist in formatting the laboratory "
        "submission report, organizing the configuration content, and generating the terminal test verification "
        "artifact in accordance with the SCSE3040 course academic integrity policy."
    )
    ai_box = Table([[Paragraph(ai_text, body_style)]], colWidths=[515])
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
        canvas.drawString(40, 22, "SCSE3040: Machine Learning Operations — Practical 05 Lab Submission")
        canvas.drawRightString(555, 22, f"Roll No: S24CSEU2521  |  Page {doc.page} of 2")
        canvas.restoreState()

    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    file_size_mb = os.path.getsize(pdf_filename) / (1024 * 1024)
    print(f"Successfully generated {pdf_filename} ({file_size_mb:.2f} MB)")

if __name__ == "__main__":
    generate_pdf()
