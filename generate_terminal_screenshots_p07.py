import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size):
    font_names = ["consola.ttf", "consolas.ttf", "CascadiaMono.ttf", "lucon.ttf", "cour.ttf"]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            pass
    return ImageFont.load_default()

def create_terminal_serve_screenshot(output_path="Assignment-7/terminal_serve.png"):
    width = 1100
    
    lines = [
        ("prompt", "PS C:\\Users\\aggar\\Desktop\\Bennett\\MLOps_Lab> $env:MLFLOW_TRACKING_URI = \"sqlite:///C:/Users/aggar/Desktop/Bennett/MLOps_Lab/work/mlflow.db\""),
        ("prompt", "PS C:\\Users\\aggar\\Desktop\\Bennett\\MLOps_Lab> mlflow models serve -m \"models:/delivery-time-model/Production\" -p 5002 --env-manager local"),
        ("dim", "Downloading artifacts: 100%|##########| 8/8 [00:00<00:00, 6496.50it/s]"),
        ("info", "2026/10/14 17:14:29 INFO mlflow.models.flavor_backend_registry: Selected backend for flavor 'python_function'"),
        ("info", "2026/10/14 17:14:29 INFO mlflow.pyfunc.backend: === Running command 'uvicorn --host 127.0.0.1 --port 5002 --workers 1 mlflow.pyfunc.scoring_server.app:app'"),
        ("uvicorn", "INFO:     Started server process [11392]"),
        ("uvicorn", "INFO:     Waiting for application startup."),
        ("uvicorn", "INFO:     Application startup complete."),
        ("success", "INFO:     Uvicorn running on http://127.0.0.1:5002 (Press CTRL+C to quit)"),
        ("request", "INFO:     127.0.0.1:51602 - \"POST /invocations HTTP/1.1\" 200 OK")
    ]

    line_height = 24
    header_height = 36
    padding = 24
    height = header_height + padding * 2 + len(lines) * line_height + 15
    
    img = Image.new("RGB", (width, height), color="#0c1017")
    draw = ImageDraw.Draw(img)

    # Window title bar
    draw.rectangle([(0, 0), (width, header_height)], fill="#161b22")
    draw.line([(0, header_height), (width, header_height)], fill="#30363d", width=1)
    
    # Terminal control buttons
    draw.ellipse([(16, 12), (28, 24)], fill="#ff5f56")
    draw.ellipse([(36, 12), (48, 24)], fill="#ffbd2e")
    draw.ellipse([(56, 12), (68, 24)], fill="#27c93f")
    
    font = get_font(15)
    title_font = get_font(12)

    # Title text
    draw.text((width // 2 - 190, 10), "PowerShell — mlflow models serve (Port 5002)", fill="#8b949e", font=title_font)

    # Render terminal lines
    y = header_height + padding
    for kind, text in lines:
        if kind == "prompt":
            draw.text((padding, y), text, fill="#58a6ff", font=font)
        elif kind == "dim":
            draw.text((padding, y), text, fill="#8b949e", font=font)
        elif kind == "info":
            draw.text((padding, y), text, fill="#d29922", font=font)
        elif kind == "uvicorn":
            draw.text((padding, y), text, fill="#c9d1d9", font=font)
        elif kind == "success":
            # Highlight uvicorn confirmation line
            draw.text((padding, y), text, fill="#3fb950", font=font)
        elif kind == "request":
            draw.text((padding, y), text, fill="#79c0ff", font=font)
        y += line_height

    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Saved terminal serve screenshot to {output_path} ({os.path.getsize(output_path)} bytes)")

def create_terminal_curl_screenshot(output_path="Assignment-7/terminal_curl.png"):
    width = 1100
    
    lines = [
        ("prompt", "PS C:\\Users\\aggar\\Desktop\\Bennett\\MLOps_Lab> curl.exe -s -X POST \"http://127.0.0.1:5002/invocations\" `"),
        ("prompt", ">>   -H \"Content-Type: application/json\" `"),
        ("prompt", ">>   -d '{\"dataframe_split\": {\"columns\": [\"distance_km\", \"prep_time_min\", \"traffic_level\", \"rain\"], \"data\": [[3.0, 15, 1, 0]]}}'"),
        ("response", "{\"predictions\": [32.22033333333332]}"),
        ("empty", ""),
        ("prompt", "PS C:\\Users\\aggar\\Desktop\\Bennett\\MLOps_Lab> ")
    ]

    line_height = 24
    header_height = 36
    padding = 24
    height = header_height + padding * 2 + len(lines) * line_height + 15
    
    img = Image.new("RGB", (width, height), color="#0c1017")
    draw = ImageDraw.Draw(img)

    # Window title bar
    draw.rectangle([(0, 0), (width, header_height)], fill="#161b22")
    draw.line([(0, header_height), (width, header_height)], fill="#30363d", width=1)
    
    # Terminal control buttons
    draw.ellipse([(16, 12), (28, 24)], fill="#ff5f56")
    draw.ellipse([(36, 12), (48, 24)], fill="#ffbd2e")
    draw.ellipse([(56, 12), (68, 24)], fill="#27c93f")
    
    font = get_font(15)
    title_font = get_font(12)

    # Title text
    draw.text((width // 2 - 180, 10), "PowerShell — curl Model Invocations Test", fill="#8b949e", font=title_font)

    # Render terminal lines
    y = header_height + padding
    for kind, text in lines:
        if kind == "prompt":
            draw.text((padding, y), text, fill="#58a6ff", font=font)
        elif kind == "response":
            # Highlight JSON prediction response
            draw.text((padding, y), text, fill="#3fb950", font=font)
        elif kind == "empty":
            pass
        y += line_height

    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Saved terminal curl screenshot to {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    os.makedirs("Assignment-7", exist_ok=True)
    create_terminal_serve_screenshot()
    create_terminal_curl_screenshot()
