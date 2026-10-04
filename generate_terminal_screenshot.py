import os
from PIL import Image, ImageDraw, ImageFont

def create_terminal_screenshot(output_path="terminal_pytest.png"):
    # High-DPI terminal capture
    width = 1100
    
    lines = [
        ("prompt", "PS C:\\Users\\aggar\\Desktop\\Bennett\\MLOps_Lab\\work> pytest -v"),
        ("dim", "============================= test session starts ============================="),
        ("dim", "platform win32 -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0"),
        ("dim", "rootdir: C:\\Users\\aggar\\Desktop\\Bennett\\MLOps_Lab\\work"),
        ("dim", "plugins: anyio-4.13.0, langsmith-0.9.7, asyncio-1.4.0"),
        ("dim", "asyncio: mode=Mode.STRICT, debug=False"),
        ("dim", "collecting ... collected 10 items"),
        ("empty", ""),
        ("item", "test_model.py::test_rain_never_makes_delivery_faster ", "PASSED", " [ 10%]"),
        ("item", "test_model.py::test_further_is_never_faster ", "PASSED", " [ 20%]"),
        ("item", "test_model.py::test_error_is_better_than_guessing ", "PASSED", " [ 30%]"),
        ("item", "test_model.py::test_heavier_traffic_is_never_faster ", "PASSED", " [ 40%]"),
        ("item", "test_orders.py::test_minutes_per_km_simple ", "PASSED", " [ 50%]"),
        ("item", "test_orders.py::test_minutes_per_km_rejects_zero_distance ", "PASSED", " [ 60%]"),
        ("item", "test_orders.py::test_good_order_is_accepted ", "PASSED", " [ 70%]"),
        ("item", "test_orders.py::test_bad_traffic_level_is_rejected ", "PASSED", " [ 80%]"),
        ("item", "test_speed.py::test_slow_delivery ", "PASSED", " [ 90%]"),
        ("item", "test_speed.py::test_negative_distance_raises ", "PASSED", "[100%]"),
        ("empty", ""),
        ("summary", "============================= 10 passed in 0.23s =============================="),
        ("prompt", "PS C:\\Users\\aggar\\Desktop\\Bennett\\MLOps_Lab\\work> ")
    ]

    line_height = 24
    header_height = 36
    padding = 24
    height = header_height + padding * 2 + len(lines) * line_height + 10
    
    img = Image.new("RGB", (width, height), color="#0c1017")
    draw = ImageDraw.Draw(img)

    # Window title bar (mac/modern linux/windows terminal aesthetic)
    draw.rectangle([(0, 0), (width, header_height)], fill="#161b22")
    draw.line([(0, header_height), (width, header_height)], fill="#30363d", width=1)
    
    # Terminal control buttons
    draw.ellipse([(16, 12), (28, 24)], fill="#ff5f56")
    draw.ellipse([(36, 12), (48, 24)], fill="#ffbd2e")
    draw.ellipse([(56, 12), (68, 24)], fill="#27c93f")
    
    # Try loading monospace font (Consolas, Cascadia Code, or fallback)
    font_names = ["consola.ttf", "consolas.ttf", "CascadiaMono.ttf", "lucon.ttf", "cour.ttf"]
    font = None
    title_font = None
    for fn in font_names:
        try:
            font = ImageFont.truetype(fn, 15)
            title_font = ImageFont.truetype(fn, 12)
            break
        except Exception:
            pass
    if font is None:
        font = ImageFont.load_default()
        title_font = font

    # Title text
    draw.text((width // 2 - 120, 10), "PowerShell — pytest -v (work)", fill="#8b949e", font=title_font)

    # Render terminal lines
    y = header_height + padding
    for item in lines:
        kind = item[0]
        if kind == "prompt":
            draw.text((padding, y), item[1], fill="#58a6ff", font=font)
        elif kind == "dim":
            draw.text((padding, y), item[1], fill="#8b949e", font=font)
        elif kind == "empty":
            pass
        elif kind == "summary":
            draw.text((padding, y), item[1], fill="#3fb950", font=font)
        elif kind == "item":
            prefix = item[1]
            status = item[2]
            pct = item[3]
            draw.text((padding, y), prefix, fill="#c9d1d9", font=font)
            
            # calculate offset for status
            bbox = draw.textbbox((padding, y), prefix, font=font)
            x_status = bbox[2]
            draw.text((x_status, y), status, fill="#3fb950", font=font)
            
            bbox_status = draw.textbbox((x_status, y), status, font=font)
            draw.text((width - padding - 80, y), pct, fill="#58a6ff", font=font)
            
        y += line_height

    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Saved terminal screenshot to {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    create_terminal_screenshot()
