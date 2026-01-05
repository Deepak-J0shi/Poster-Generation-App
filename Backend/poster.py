from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests, os, random, base64
from typing import Optional, Tuple

# ========== LAYOUT CONTROLS ==========

# Full poster size (1080x1920 for reels, or 1080x1350 for insta)
OUTPUT_SIZE: Tuple[int, int] = (1080, 1920)

# Relative heights (fractions of total height)
TOP_RATIO: float = 0.18       # top empty space for salon name
BOTTOM_RATIO: float = 0.20    # bottom CTA band

# ========== PATHS ==========

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# AI-generated base posters: assets/base1.png, base2.png, ...
BASE_POSTERS = [
    os.path.join(ASSETS_DIR, f)
    for f in os.listdir(ASSETS_DIR)
    if f.startswith("base") and f.lower().endswith(".png")
]

# Font file
FONT_PATH = os.path.join(BASE_DIR, "Poppins-Regular.ttf")

# Static logos
APP_LOGO_PATH = os.path.join(ASSETS_DIR, "app_logo.png")     # Glownify logo
STORE_BADGE_PATH = os.path.join(ASSETS_DIR, "app_icons.png") # Combined Play + App Store badge


# ========== HELPERS ==========

def _load_font(size: int = 36) -> ImageFont.FreeTypeFont:
    """Load scalable TTF font; fall back to default if missing."""
    try:
        if os.path.exists(FONT_PATH):
            return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        pass
    return ImageFont.load_default()


def _safe_open_image(path: str) -> Optional[Image.Image]:
    try:
        if os.path.exists(path):
            return Image.open(path).convert("RGBA")
    except Exception:
        pass
    return None


def fetch_image_from_url(url: str) -> Optional[Image.Image]:
    """Support normal URL + base64 data URL."""
    if not url:
        return None
    try:
        if url.startswith("data:"):
            _, data = url.split(",", 1)
            img_data = base64.b64decode(data)
            return Image.open(BytesIO(img_data)).convert("RGBA")
        else:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            return Image.open(BytesIO(r.content)).convert("RGBA")
    except Exception:
        return None


# ========== MAIN FUNCTION ==========

def create_poster(
    salon_name: str,
    logo_image: Optional[Image.Image],
    contact: str,
    website: str,
    offer: str,
    address: str,
    output_size: Tuple[int, int] = OUTPUT_SIZE,
) -> bytes:

    if not BASE_POSTERS:
        raise FileNotFoundError("No base*.png poster images in assets/ folder")

    W, H = output_size
    top_h = int(H * TOP_RATIO)
    bottom_h = int(H * BOTTOM_RATIO)
    mid_h = H - top_h - bottom_h

    # Base white background
    final = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(final, "RGBA")

    # ========== MID: AI BASE IMAGE ==========
    base = Image.open(random.choice(BASE_POSTERS)).convert("RGBA")
    base = base.resize((W, mid_h))
    final.paste(base, (0, top_h))

    # ========== TOP: SALON NAME BAND ==========
    draw.rectangle([(0, 0), (W, top_h)], fill=(249, 245, 250, 255))

    title_font_size = int(W * 0.11)
    title_font = _load_font(title_font_size)
    text = salon_name.strip() or "Your Salon Name"

    bbox = draw.textbbox((0, 0), text, font=title_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (W - tw) // 2
    ty = (top_h - th) // 2

    draw.text((tx, ty), text, font=title_font, fill=(45, 25, 35))

    # Optional salon logo inside top band
    if logo_image:
        logo = logo_image.copy()
        logo.thumbnail((int(top_h * 0.6), int(top_h * 0.6)))
        lx = int(W * 0.04)
        ly = (top_h - logo.size[1]) // 2
        final.paste(logo, (lx, ly), logo)

    # ========== BOTTOM CTA BAND ==========
    bottom_y = H - bottom_h
    draw.rectangle([(0, bottom_y), (W, H)], fill=(255, 252, 247, 255))

    margin_x = int(W * 0.06)

    # ---- OFFER TEXT (ABOVE LOGOS) ----
        # ---- OFFER TEXT (ABOVE LOGOS) ----
    RAW_PLACEHOLDER = r"50% off on any service"

    offer_text = (offer or "").strip()

    # Agar user ne kuch nahin likha ya placeholder hi aa gaya,
    # to default tagline use karo
    if (not offer_text) or (offer_text.lower() == RAW_PLACEHOLDER.lower()):
        offer_text = "Book salon appointments instantly and call beauticians at home"


    # Start with a reasonable font size and shrink if too wide
    offer_font_size = int(W * 0.045)  # ~48px on 1080 width
    offer_font = _load_font(offer_font_size)

    max_text_width = W - 2 * margin_x
    bbox = draw.textbbox((0, 0), offer_text, font=offer_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    while tw > max_text_width and offer_font_size > 18:
        offer_font_size -= 2
        offer_font = _load_font(offer_font_size)
        bbox = draw.textbbox((0, 0), offer_text, font=offer_font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

    offer_x = (W - tw) // 2
    # place near top of bottom band so it's just under the main image
    offer_y = bottom_y + int(bottom_h * 0.12)
    draw.text((offer_x, offer_y), offer_text, font=offer_font, fill=(60, 40, 35))

    # ---- Load logos ----
    left_logo = _safe_open_image(APP_LOGO_PATH)        # Glownify logo
    store_badge = _safe_open_image(STORE_BADGE_PATH)   # Play + App Store badge

    # We'll place logos a bit lower than before so offer is clearly visible
    logos_center_y = bottom_y + int(bottom_h * 0.70)

    # ---- LEFT: Glownify app logo ----
    if left_logo:
        max_h = int(bottom_h * 0.60)
        left_logo = left_logo.copy()
        left_logo.thumbnail((max_h, max_h))
        lx = margin_x
        ly = logos_center_y - left_logo.size[1] // 2
        final.paste(left_logo, (lx, ly), left_logo)

    # ---- RIGHT: Store badge icons (Download now) ----
    if store_badge:
        max_h = int(bottom_h * 0.70)
        store_badge = store_badge.copy()
        store_badge.thumbnail((W, max_h))
        bx = W - margin_x - store_badge.size[0]
        by = logos_center_y - store_badge.size[1] // 2
        final.paste(store_badge, (bx, by), store_badge)

    # ========== EXPORT ==========
    out = BytesIO()
    final.save(out, format="PNG", quality=100)
    out.seek(0)
    return out.read()
