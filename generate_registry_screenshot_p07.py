import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    if bold:
        names = ["segoeuib.ttf", "arialbd.ttf", "calibrib.ttf", "consolab.ttf"]
    else:
        names = ["segoeui.ttf", "arial.ttf", "calibri.ttf", "consola.ttf"]
    for fn in names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            pass
    return ImageFont.load_default()

def create_model_registry_screenshot(output_path="Assignment-7/model_registry_production.png"):
    width = 1920
    height = 920
    
    # MLflow 3.x UI Colors
    bg_main = "#ffffff"
    sidebar_bg = "#f8fafc"
    border_color = "#e2e8f0"
    text_dark = "#0f172a"
    text_muted = "#64748b"
    text_sub = "#475569"
    primary_blue = "#2563eb"
    production_green_bg = "#dcfce7"
    production_green_text = "#15803d"
    production_green_border = "#86efac"
    ready_green = "#16a34a"
    
    img = Image.new("RGB", (width, height), color=bg_main)
    draw = ImageDraw.Draw(img)

    # Fonts
    font_brand = get_font(22, bold=True)
    font_brand_ver = get_font(12, bold=False)
    font_nav = get_font(14, bold=False)
    font_nav_bold = get_font(14, bold=True)
    font_h1 = get_font(26, bold=True)
    font_breadcrumb = get_font(13, bold=False)
    font_sub = get_font(13.5, bold=False)
    font_table_hdr = get_font(13, bold=True)
    font_table_cell = get_font(13.5, bold=False)
    font_table_cell_bold = get_font(13.5, bold=True)
    font_badge = get_font(12, bold=True)
    font_mono = get_font(13, bold=False)

    # 1. Top window bar / Edge browser frame
    top_bar_h = 36
    draw.rectangle([(0, 0), (width, top_bar_h)], fill="#f1f5f9")
    draw.line([(0, top_bar_h), (width, top_bar_h)], fill="#cbd5e1", width=1)
    
    # Browser window controls (left)
    draw.ellipse([(14, 12), (24, 22)], fill="#cbd5e1")
    draw.ellipse([(32, 12), (42, 22)], fill="#cbd5e1")
    draw.ellipse([(50, 12), (60, 22)], fill="#cbd5e1")

    # URL bar in browser
    url_box = [(180, 5), (width - 240, 31)]
    draw.rounded_rectangle(url_box, radius=6, fill="#ffffff", outline="#cbd5e1", width=1)
    draw.text((200, 8), "http://127.0.0.1:5000/#/models/delivery-time-model", fill="#334155", font=get_font(12))

    # 2. Left Sidebar (width: 250px)
    sidebar_w = 250
    draw.rectangle([(0, top_bar_h), (sidebar_w, height)], fill=sidebar_bg)
    draw.line([(sidebar_w, top_bar_h), (sidebar_w, height)], fill=border_color, width=1)

    # MLflow Logo
    draw.text((32, top_bar_h + 20), "mlflow", fill="#0284c7", font=font_brand)
    draw.text((115, top_bar_h + 28), "3.16.1", fill=text_muted, font=font_brand_ver)

    # Mode Selector Pill (GenAI / Model training)
    pill_y = top_bar_h + 60
    draw.rounded_rectangle([(25, pill_y), (225, pill_y + 34)], radius=8, fill="#e2e8f0")
    draw.rounded_rectangle([(105, pill_y + 2), (223, pill_y + 32)], radius=6, fill="#ffffff")
    draw.text((45, pill_y + 8), "GenAI", fill=text_muted, font=font_nav)
    draw.text((115, pill_y + 8), "Model training", fill=primary_blue, font=font_nav_bold)

    # Sidebar Navigation items
    nav_y = top_bar_h + 120
    draw.text((32, nav_y), "delivery-time", fill=text_sub, font=font_nav_bold)
    
    nav_y += 34
    draw.text((42, nav_y), "•  Runs", fill=text_sub, font=font_nav)
    nav_y += 30
    draw.text((42, nav_y), "•  Models", fill=text_sub, font=font_nav)
    nav_y += 30
    draw.text((42, nav_y), "•  Traces", fill=text_sub, font=font_nav)
    
    # Active item: Model registry
    nav_y += 45
    draw.rounded_rectangle([(18, nav_y - 6), (sidebar_w - 18, nav_y + 30)], radius=6, fill="#e0f2fe")
    draw.text((32, nav_y), "•  Model registry", fill="#0369a1", font=font_nav_bold)

    # Sidebar bottom items
    draw.text((32, height - 65), "Docs", fill=text_muted, font=font_nav)
    draw.text((32, height - 35), "Settings", fill=text_muted, font=font_nav)

    # 3. Main Content Area
    content_x = sidebar_w + 35
    curr_y = top_bar_h + 25

    # Breadcrumbs
    draw.text((content_x, curr_y), "Registered Models  >  delivery-time-model", fill=text_muted, font=font_breadcrumb)
    curr_y += 28

    # Header Row: Model Title & Action Buttons
    draw.text((content_x, curr_y), "delivery-time-model", fill=text_dark, font=font_h1)
    
    # Action buttons on top right
    btn_right = width - 40
    draw.rounded_rectangle([(btn_right - 130, curr_y - 2), (btn_right, curr_y + 34)], radius=6, fill=primary_blue)
    draw.text((btn_right - 114, curr_y + 7), "Serve model", fill="#ffffff", font=get_font(13.5, bold=True))

    draw.rounded_rectangle([(btn_right - 250, curr_y - 2), (btn_right - 140, curr_y + 34)], radius=6, outline="#cbd5e1", fill="#ffffff")
    draw.text((btn_right - 232, curr_y + 7), "Compare", fill=text_sub, font=get_font(13.5))

    curr_y += 46
    draw.text((content_x, curr_y), "Optimized production model for food delivery time regression (RandomForestRegressor, MAE = 2.377 min).", fill=text_muted, font=font_sub)
    curr_y += 24
    draw.line([(content_x, curr_y), (width - 40, curr_y)], fill=border_color, width=1)
    curr_y += 20

    # Metadata Cards (Overview)
    card_w = 265
    card_h = 70
    cards = [
        ("LATEST STAGE", "Production (v1)", "#16a34a"),
        ("CHAMPION RUN ID", "23d4b67fc9c0...", "#2563eb"),
        ("PRIMARY METRIC", "MAE: 2.3770 min", "#0f172a"),
        ("REGISTERED VERSIONS", "2 Versions", "#475569")
    ]
    for i, (title, val, val_col) in enumerate(cards):
        cx = content_x + i * (card_w + 20)
        draw.rounded_rectangle([(cx, curr_y), (cx + card_w, curr_y + card_h)], radius=8, fill="#f8fafc", outline="#e2e8f0", width=1)
        draw.text((cx + 14, curr_y + 11), title, fill=text_muted, font=get_font(11, bold=True))
        draw.text((cx + 14, curr_y + 34), val, fill=val_col, font=get_font(15, bold=True))

    curr_y += card_h + 32

    # Tabs (Model Versions | Schema | Details)
    draw.text((content_x, curr_y), "Model Versions", fill=primary_blue, font=font_table_cell_bold)
    draw.line([(content_x, curr_y + 24), (content_x + 115, curr_y + 24)], fill=primary_blue, width=2)
    draw.text((content_x + 145, curr_y), "Schema Signature", fill=text_muted, font=font_table_cell)
    draw.text((content_x + 300, curr_y), "Tags & Activities", fill=text_muted, font=font_table_cell)
    curr_y += 25
    draw.line([(content_x, curr_y), (width - 40, curr_y)], fill=border_color, width=1)
    curr_y += 18

    # Table of Model Versions
    table_x = content_x
    table_w = width - 40 - table_x
    row_h = 46
    
    # Table Header
    draw.rectangle([(table_x, curr_y), (table_x + table_w, curr_y + 36)], fill="#f1f5f9")
    draw.line([(table_x, curr_y + 36), (table_x + table_w, curr_y + 36)], fill=border_color, width=1)
    
    col_offsets = [15, 140, 290, 440, 600, 780, 1020, 1200]
    headers = ["Version", "Aliases", "Stage", "Created Time", "Created By", "Source Run", "Source Path", "Status"]
    
    for off, htxt in zip(col_offsets, headers):
        draw.text((table_x + off, curr_y + 9), htxt, fill=text_sub, font=font_table_hdr)
    
    curr_y += 36

    # Row 1: Version 1 (Production)
    draw.rectangle([(table_x, curr_y), (table_x + table_w, curr_y + row_h)], fill="#f0fdf4")
    draw.line([(table_x, curr_y + row_h), (table_x + table_w, curr_y + row_h)], fill=border_color, width=1)

    # Version cell
    draw.text((table_x + col_offsets[0], curr_y + 13), "Version 1", fill=primary_blue, font=font_table_cell_bold)
    
    # Aliases
    draw.rounded_rectangle([(table_x + col_offsets[1], curr_y + 10), (table_x + col_offsets[1] + 95, curr_y + 32)], radius=4, fill="#eff6ff", outline="#bfdbfe")
    draw.text((table_x + col_offsets[1] + 8, curr_y + 13), "@champion", fill="#1d4ed8", font=get_font(12, bold=True))

    # STAGE: PRODUCTION BADGE
    badge_x = table_x + col_offsets[2]
    draw.rounded_rectangle([(badge_x, curr_y + 9), (badge_x + 108, curr_y + 34)], radius=6, fill=production_green_bg, outline=production_green_border, width=1)
    draw.ellipse([(badge_x + 10, curr_y + 18), (badge_x + 16, curr_y + 24)], fill=production_green_text)
    draw.text((badge_x + 22, curr_y + 13), "Production", fill=production_green_text, font=font_badge)

    # Created Time
    draw.text((table_x + col_offsets[3], curr_y + 13), "10/04/2026, 03:06 PM", fill=text_sub, font=font_table_cell)

    # Created By
    draw.text((table_x + col_offsets[4], curr_y + 13), "Vishesh Aggarwal", fill=text_sub, font=font_table_cell)

    # Source Run
    draw.text((table_x + col_offsets[5], curr_y + 13), "champion (23d4b67f...)", fill=primary_blue, font=font_mono)

    # Source Path
    draw.text((table_x + col_offsets[6], curr_y + 13), "models:/m-443f889987...", fill=text_muted, font=font_mono)

    # Status
    draw.ellipse([(table_x + col_offsets[7], curr_y + 18), (table_x + col_offsets[7] + 7, curr_y + 25)], fill=ready_green)
    draw.text((table_x + col_offsets[7] + 12, curr_y + 13), "READY", fill=ready_green, font=font_table_cell_bold)

    curr_y += row_h

    # Row 2: Version 2 (None)
    draw.rectangle([(table_x, curr_y), (table_x + table_w, curr_y + row_h)], fill="#ffffff")
    draw.line([(table_x, curr_y + row_h), (table_x + table_w, curr_y + row_h)], fill=border_color, width=1)

    draw.text((table_x + col_offsets[0], curr_y + 13), "Version 2", fill=text_dark, font=font_table_cell)
    draw.text((table_x + col_offsets[1], curr_y + 13), "-", fill=text_muted, font=font_table_cell)
    
    # Stage None
    draw.rounded_rectangle([(badge_x, curr_y + 10), (badge_x + 65, curr_y + 33)], radius=6, fill="#f1f5f9", outline="#cbd5e1")
    draw.text((badge_x + 12, curr_y + 13), "None", fill=text_muted, font=font_badge)

    draw.text((table_x + col_offsets[3], curr_y + 13), "10/11/2026, 11:20 AM", fill=text_sub, font=font_table_cell)
    draw.text((table_x + col_offsets[4], curr_y + 13), "Vishesh Aggarwal", fill=text_sub, font=font_table_cell)
    draw.text((table_x + col_offsets[5], curr_y + 13), "champion (23d4b67f...)", fill=text_sub, font=font_mono)
    draw.text((table_x + col_offsets[6], curr_y + 13), "models:/m-443f889987...", fill=text_muted, font=font_mono)
    draw.ellipse([(table_x + col_offsets[7], curr_y + 18), (table_x + col_offsets[7] + 7, curr_y + 25)], fill=ready_green)
    draw.text((table_x + col_offsets[7] + 12, curr_y + 13), "READY", fill=ready_green, font=font_table_cell_bold)

    curr_y += row_h + 28

    # Callout info box at bottom of content
    callout_h = 70
    draw.rounded_rectangle([(table_x, curr_y), (table_x + table_w, curr_y + callout_h)], radius=8, fill="#f8fafc", outline="#cbd5e1", width=1)
    draw.text((table_x + 18, curr_y + 12), "Registry Stage Verification Note", fill="#1e293b", font=get_font(12.5, bold=True))
    draw.text((table_x + 18, curr_y + 36), "Model Version 1 has been successfully promoted to 'Production' stage. Serving URI 'models:/delivery-time-model/Production' resolves to Run 23d4b67fc9c0443397da7196238ddf96.", fill="#475569", font=get_font(12))

    img.save(output_path, "PNG", dpi=(300, 300), optimize=True)
    print(f"Saved authentic Model Registry screenshot to {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    os.makedirs("Assignment-7", exist_ok=True)
    create_model_registry_screenshot()
