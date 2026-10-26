import os
from PIL import Image

# Assignment-6 screenshot paths
img_runs_table = "Assignment-6/Screenshot 2026-10-04 150544.png"
img_best_run = "Assignment-6/Screenshot 2026-10-04 150615.png"
img_artifacts = "Assignment-6/Screenshot 2026-10-04 150629.png"

# Process runs table screenshot
# Crop outer window border / top browser tab bar if desired, or keep clean browser view
im_runs = Image.open(img_runs_table).convert("RGB")
# Dimensions: (1918, 897)
# Let's crop away excessive whitespace or bottom bar if needed
# The main content area:
# X: 0 to 1918 (or 160 to 1900)
# Y: 25 to 870
w, h = im_runs.size
print(f"im_runs size: {w}x{h}")
crop_runs = im_runs.crop((0, 20, w, h - 30))
crop_runs.save("crop_runs_table.png", "PNG", optimize=True)

# Process best run detail screenshot
im_best = Image.open(img_best_run).convert("RGB")
wb, hb = im_best.size
print(f"im_best size: {wb}x{hb}")
crop_best = im_best.crop((0, 20, wb, hb - 30))
crop_best.save("crop_best_run.png", "PNG", optimize=True)

# Also check artifacts
im_art = Image.open(img_artifacts).convert("RGB")
wa, ha = im_art.size
crop_art = im_art.crop((0, 20, wa, ha - 30))
crop_art.save("crop_artifacts.png", "PNG", optimize=True)

print("Images cropped and saved successfully.")
