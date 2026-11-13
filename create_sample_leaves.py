"""
Generates sample leaf images for testing Leaf Doctor.
"""
from PIL import Image, ImageDraw
from pathlib import Path

LEAF_DIR = Path(__file__).resolve().parent / "data" / "sample_leaves"
LEAF_DIR.mkdir(parents=True, exist_ok=True)

# 1. Healthy Leaf (Vibrant Green)
healthy = Image.new("RGB", (200, 200), color=(240, 248, 240))
draw = ImageDraw.Draw(healthy)
# Draw oval leaf shape
draw.ellipse([30, 20, 170, 180], fill=(46, 139, 87), outline=(34, 100, 60), width=3)
# Draw leaf veins
draw.line([100, 20, 100, 180], fill=(144, 238, 144), width=3)
draw.line([100, 70, 50, 50], fill=(144, 238, 144), width=2)
draw.line([100, 70, 150, 50], fill=(144, 238, 144), width=2)
draw.line([100, 120, 50, 100], fill=(144, 238, 144), width=2)
draw.line([100, 120, 150, 100], fill=(144, 238, 144), width=2)
healthy.save(LEAF_DIR / "healthy_leaf.png")

# 2. Sick Leaf (Yellow with Brown Spots / Blast)
sick = Image.new("RGB", (200, 200), color=(255, 250, 240))
draw = ImageDraw.Draw(sick)
# Draw pale yellow-green leaf
draw.ellipse([30, 20, 170, 180], fill=(218, 165, 32), outline=(139, 69, 19), width=3)
# Brown disease spots
draw.ellipse([70, 50, 95, 75], fill=(139, 69, 19))
draw.ellipse([120, 80, 145, 105], fill=(139, 69, 19))
draw.ellipse([60, 110, 85, 135], fill=(120, 50, 20))
draw.ellipse([110, 130, 130, 150], fill=(120, 50, 20))
sick.save(LEAF_DIR / "sick_leaf.png")

print("Created sample leaves successfully!")

