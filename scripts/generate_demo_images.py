"""
Generate rich realistic sample craft images for KalaiPaalam AI Studio demonstrations.
Produces both RAW (artisan workshop setting with background noise/shadows)
and CATALOG (AI Studio background removed, lighting enhanced, subtle pedestal shadow).
"""

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np
import os

IMG_DIR = r"C:\Users\ANDREWS\.gemini\antigravity\scratch\kalai-paalam\backend\app\static\images"
DATA_DIR = r"C:\Users\ANDREWS\.gemini\antigravity\scratch\kalai-paalam\data\images"
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

def generate_saree_images():
    width, height = 800, 800

    # 1. Raw Saree on workshop wooden plank with warm shadow
    raw = Image.new("RGB", (width, height), (198, 166, 132))
    draw_raw = ImageDraw.Draw(raw)
    # Add wood grain lines
    for y in range(0, height, 25):
        draw_raw.line([(0, y), (width, y + 10)], fill=(175, 142, 108), width=2)
    # Workshop clutter / shadow
    draw_raw.ellipse([(150, 480), (650, 680)], fill=(120, 95, 70))
    # Saree drape fold
    # Main fabric body - Royal Blue with texture
    draw_raw.polygon([(200, 200), (600, 180), (640, 560), (160, 580)], fill=(22, 58, 138))
    # Saree weave texture lines
    for i in range(210, 590, 8):
        draw_raw.line([(i, 195), (i - 20, 570)], fill=(32, 75, 175), width=1)
    # Floral Maroon & Gold Zari Border
    draw_raw.polygon([(160, 520), (640, 500), (645, 570), (155, 590)], fill=(128, 15, 36))
    for x in range(170, 630, 22):
        draw_raw.ellipse([(x, 525), (x + 14, 545)], fill=(212, 175, 55)) # Gold motifs
        draw_raw.ellipse([(x + 4, 548), (x + 10, 554)], fill=(240, 210, 90))
    # Uneven raw lighting gradient
    raw = raw.filter(ImageFilter.GaussianBlur(0.6))
    raw.save(os.path.join(IMG_DIR, "saree_raw.jpg"), quality=90)
    raw.save(os.path.join(DATA_DIR, "saree_raw.jpg"), quality=90)

    # 2. Studio Catalog Saree - Pristine off-white studio background with soft contact shadow
    cat = Image.new("RGB", (width, height), (248, 249, 250))
    draw_cat = ImageDraw.Draw(cat)
    # Soft modern studio contact shadow
    shadow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d_shadow = ImageDraw.Draw(shadow)
    d_shadow.ellipse([(160, 560), (640, 620)], fill=(0, 0, 0, 45))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    cat.paste(shadow, (0, 0), shadow)
    # Sharp, lighting-corrected, vibrant fabric
    draw_cat.polygon([(200, 200), (600, 180), (640, 560), (160, 580)], fill=(28, 72, 170))
    for i in range(210, 590, 8):
        draw_cat.line([(i, 195), (i - 20, 570)], fill=(40, 92, 210), width=1)
    # Enhanced Zari Luster Border
    draw_cat.polygon([(160, 520), (640, 500), (645, 570), (155, 590)], fill=(145, 20, 45))
    for x in range(170, 630, 22):
        draw_cat.ellipse([(x, 525), (x + 14, 545)], fill=(235, 195, 65))
        draw_cat.ellipse([(x + 4, 548), (x + 10, 554)], fill=(255, 230, 110))
    # Subtle studio highlight edge
    draw_cat.line([(200, 200), (600, 180)], fill=(80, 130, 240), width=2)
    cat.save(os.path.join(IMG_DIR, "saree_catalog.jpg"), quality=95)
    cat.save(os.path.join(DATA_DIR, "saree_catalog.jpg"), quality=95)

def generate_brass_images():
    width, height = 800, 800

    # 1. Raw Brass Diya on dusty cement floor
    raw = Image.new("RGB", (width, height), (145, 142, 136))
    draw_raw = ImageDraw.Draw(raw)
    # Floor texture
    for _ in range(300):
        rx, ry = int(np.random.randint(0, width)), int(np.random.randint(0, height))
        draw_raw.point((rx, ry), fill=(120, 118, 112))
    # Raw Brass Peacock Diya
    # Base
    draw_raw.ellipse([(280, 520), (520, 580)], fill=(150, 120, 50))
    # Stem
    draw_raw.rectangle([(380, 360), (420, 530)], fill=(165, 130, 55))
    # Oil bowl
    draw_raw.arc([(310, 340), (490, 410)], 0, 180, fill=(180, 145, 60), width=15)
    # Peacock arch
    draw_raw.ellipse([(350, 220), (450, 340)], fill=(170, 135, 55))
    draw_raw.polygon([(400, 200), (420, 230), (380, 230)], fill=(190, 155, 65))
    raw.save(os.path.join(IMG_DIR, "brass_raw.jpg"), quality=90)
    raw.save(os.path.join(DATA_DIR, "brass_raw.jpg"), quality=90)

    # 2. Catalog Brass Diya - Clean, glowing metallic luster
    cat = Image.new("RGB", (width, height), (250, 250, 250))
    shadow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d_shadow = ImageDraw.Draw(shadow)
    d_shadow.ellipse([(260, 545), (540, 595)], fill=(0, 0, 0, 50))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    cat.paste(shadow, (0, 0), shadow)

    draw_cat = ImageDraw.Draw(cat)
    # Radiant warm brass colors
    draw_cat.ellipse([(280, 520), (520, 580)], fill=(190, 150, 60))
    draw_cat.rectangle([(380, 360), (420, 530)], fill=(205, 165, 70))
    draw_cat.arc([(310, 340), (490, 410)], 0, 180, fill=(225, 180, 80), width=16)
    draw_cat.ellipse([(350, 220), (450, 340)], fill=(215, 170, 75))
    # Specular metallic highlights
    draw_cat.line([(390, 370), (390, 520)], fill=(255, 235, 160), width=3)
    draw_cat.ellipse([(380, 250), (400, 270)], fill=(255, 240, 180))
    cat.save(os.path.join(IMG_DIR, "brass_catalog.jpg"), quality=95)
    cat.save(os.path.join(DATA_DIR, "brass_catalog.jpg"), quality=95)

if __name__ == "__main__":
    generate_saree_images()
    generate_brass_images()
    print("Demo craft images generated successfully!")
