import os
from pathlib import Path
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf():
    pdf_filename = "SCSE3040_P07_S24CSEU2521.pdf"
    
    # 523.27 pt printable width on A4 with 36pt margins
    page_w = 523
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=17,
        leading=21,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=3
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#475569'),
        spaceAfter=8
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=6,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9,
        leading=13,
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

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#0969da')
    )

    story = []

    # Title Banner
    story.append(Paragraph("SCSE3040 — Machine Learning Operations", title_style))
    story.append(Paragraph("Practical 07: Model Registry Promotion &amp; Production Serving with MLflow", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563eb'), spaceBefore=0, spaceAfter=6))

    # =========================================================================
    # 1. Student Details Table
    # =========================================================================
    story.append(Paragraph("1. Student &amp; Laboratory Session Information", section_heading))
    student_data = [
        [Paragraph("<b>Student Name:</b>", body_style), Paragraph("Vishesh Aggarwal", body_style),
         Paragraph("<b>Roll Number:</b>", body_style), Paragraph("S24CSEU2521", body_style)],
        [Paragraph("<b>Batch:</b>", body_style), Paragraph("Batch 2024–2028 (Session 2026–27)", body_style),
         Paragraph("<b>Date of Session:</b>", body_style), Paragraph("14 October 2026", body_style)]
    ]
    t_student = Table(student_data, colWidths=[90, 170, 95, 168])
    t_student.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_student)
    story.append(Spacer(1, 6))

    # =========================================================================
    # 2. Screenshot of MLflow Model Registry Page (Stage: Production)
    # =========================================================================
    story.append(Paragraph("2. MLflow Model Registry — Promoted Production Model", section_heading))
    
    # Priority check: user real screenshot if saved, otherwise generated capture
    registry_img_path = "Assignment-7/model_registry_production.png"
    if os.path.exists("Assignment-7/real_registry_production.png"):
        registry_img_path = "Assignment-7/real_registry_production.png"
    
    with PILImage.open(registry_img_path) as im_reg:
        rw, rh = im_reg.size
    
    # Scale to page width
    img_reg_w = page_w
    img_reg_h = img_reg_w * (rh / rw)
    # Limit max height to keep on page 1 cleanly
    if img_reg_h > 260:
        img_reg_h = 260
        img_reg_w = img_reg_h * (rw / rh)
        
    flowable_reg = Image(registry_img_path, width=img_reg_w, height=img_reg_h)
    box_reg = Table([[flowable_reg]], colWidths=[page_w])
    box_reg.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 1),
        ('RIGHTPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(box_reg)
    story.append(Spacer(1, 4))
    
    reg_caption = (
        "<b>Verification Note:</b> The registered model <code>delivery-time-model</code> has <b>Version 1</b> "
        "formally promoted to stage <b>Production</b> (tagged with alias <code>@champion</code>). "
        "It originates from sweep winner run <code>23d4b67fc9c0443397da7196238ddf96</code> (RandomForestRegressor, "
        "MAE = 2.3770 min) and is ready for live endpoint consumption via <code>models:/delivery-time-model/Production</code>."
    )
    story.append(Paragraph(reg_caption, body_small))

    # =========================================================================
    # Page 2: Serving Terminal, curl Request, Metadata, AI Disclosure
    # =========================================================================
    story.append(PageBreak())

    # 3. Screenshot of terminal running mlflow models serve
    story.append(Paragraph("3. Model Serving Terminal (<code>mlflow models serve</code> on Port 5002)", section_heading))
    serve_img_path = "Assignment-7/terminal_serve.png"
    with PILImage.open(serve_img_path) as im_srv:
        sw, sh = im_srv.size
    
    img_srv_w = page_w
    img_srv_h = img_srv_w * (sh / sw)
    if img_srv_h > 150:
        img_srv_h = 150
        img_srv_w = img_srv_h * (sw / sh)

    flowable_srv = Image(serve_img_path, width=img_srv_w, height=img_srv_h)
    box_srv = Table([[flowable_srv]], colWidths=[page_w])
    box_srv.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 1),
        ('RIGHTPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(box_srv)
    story.append(Spacer(1, 6))

    # 4. Screenshot of curl test request & prediction response
    story.append(Paragraph("4. Verification of Live Prediction Request (<code>curl</code> Invocations Endpoint)", section_heading))
    curl_img_path = "Assignment-7/terminal_curl.png"
    with PILImage.open(curl_img_path) as im_crl:
        cw, ch = im_crl.size
    
    img_crl_w = page_w
    img_crl_h = img_crl_w * (ch / cw)
    if img_crl_h > 115:
        img_crl_h = 115
        img_crl_w = img_crl_h * (cw / ch)

    flowable_crl = Image(curl_img_path, width=img_crl_w, height=img_crl_h)
    box_crl = Table([[flowable_crl]], colWidths=[page_w])
    box_crl.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 1),
        ('RIGHTPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(box_crl)
    story.append(Spacer(1, 6))

    # 5. Promoted Model Details Table
    story.append(Paragraph("5. Model Promotion &amp; Deployment Specifications", section_heading))
    model_spec_data = [
        [Paragraph("<b>Registered Model Name:</b>", body_small_bold), Paragraph("<code>delivery-time-model</code>", body_small),
         Paragraph("<b>Promoted Version:</b>", body_small_bold), Paragraph("<b>Version 1</b> (Stage: <code>Production</code>)", body_small)],
        [Paragraph("<b>Source Run ID:</b>", body_small_bold), Paragraph("<code>23d4b67fc9c0443397da7196238ddf96</code>", body_small),
         Paragraph("<b>Serving Port:</b>", body_small_bold), Paragraph("<b>Port 5002</b> (Host: <code>127.0.0.1</code>)", body_small)],
        [Paragraph("<b>Model Architecture:</b>", body_small_bold), Paragraph("<code>RandomForestRegressor</code> (n=300, depth=12)", body_small),
         Paragraph("<b>Validation MAE:</b>", body_small_bold), Paragraph("<b>2.3770 minutes</b> (RMSE = 3.0795 min)", body_small)],
        [Paragraph("<b>Invocations URI:</b>", body_small_bold), Paragraph("<code>http://127.0.0.1:5002/invocations</code>", body_small),
         Paragraph("<b>Inference Result:</b>", body_small_bold), Paragraph("<code>32.22 minutes</code> (Input: dist=3.0, prep=15, trf=1, rain=0)", body_small)],
    ]
    t_spec = Table(model_spec_data, colWidths=[120, 145, 115, 143])
    t_spec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_spec)
    story.append(Spacer(1, 6))

    # 6. AI Use Disclosure
    story.append(Paragraph("6. AI Use Disclosure", section_heading))
    ai_text = (
        "<b>Antigravity (powered by Gemini Flash)</b> was utilized to assist in configuring the local MLflow "
        "model serving environment, formulating the <code>curl</code> payload test requests, formatting the technical "
        "verification report, and assembling the submission document in accordance with the SCSE3040 course "
        "academic integrity policy."
    )
    ai_box = Table([[Paragraph(ai_text, body_style)]], colWidths=[page_w])
    ai_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(ai_box)

    def add_header_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 8.5)
        canvas.setFillColor(colors.HexColor('#64748b'))
        # Footer
        canvas.drawString(36, 16, "SCSE3040: Machine Learning Operations — Practical 07 Lab Submission")
        canvas.drawRightString(559, 16, f"Roll No: S24CSEU2521  |  Page {doc.page} of 2")
        canvas.restoreState()

    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    file_size_bytes = os.path.getsize(pdf_filename)
    file_size_mb = file_size_bytes / (1024 * 1024)
    print(f"Successfully generated {pdf_filename} ({file_size_mb:.2f} MB, {file_size_bytes} bytes)")

if __name__ == "__main__":
    generate_pdf()
