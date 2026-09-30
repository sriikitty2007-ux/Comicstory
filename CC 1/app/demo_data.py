from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def _font(size: int):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "/Library/Fonts/Arial Bold.ttf",
    ]

    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()


def make_demo_image(
    path: Path,
    panel_number: int,
    title: str,
    art_style: str,
) -> None:

    image = Image.new(
        "RGB",
        (768, 768),
        (245, 232, 210),
    )

    draw = ImageDraw.Draw(image)

    title_font = _font(42)
    body_font = _font(26)

    draw.rectangle(
        (30, 30, 738, 738),
        outline=(35, 35, 35),
        width=8,
    )

    draw.text(
        (55, 55),
        f"PANEL {panel_number}",
        font=title_font,
        fill=(25, 25, 25),
    )

    draw.text(
        (55, 120),
        title[:42],
        font=body_font,
        fill=(50, 50, 50),
    )

    # Character head
    cx, cy = 384, 420

    draw.ellipse(
        (cx - 115, cy - 150, cx + 115, cy + 80),
        fill=(255, 207, 120),
        outline=(30, 30, 30),
        width=6,
    )

    # Eyes
    draw.ellipse(
        (cx - 65, cy - 90, cx - 35, cy - 60),
        fill=(20, 20, 20),
    )

    draw.ellipse(
        (cx + 35, cy - 90, cx + 65, cy - 60),
        fill=(20, 20, 20),
    )

    # Smile
    draw.arc(
        (cx - 60, cy - 20, cx + 60, cy + 60),
        10,
        170,
        fill=(30, 30, 30),
        width=5,
    )

    # Body
    draw.line(
        (cx - 150, cy + 80, cx - 190, cy + 240),
        fill=(30, 30, 30),
        width=12,
    )

    draw.line(
        (cx + 150, cy + 80, cx + 190, cy + 240),
        fill=(30, 30, 30),
        width=12,
    )

    draw.line(
        (cx - 50, cy + 60, cx - 80, cy + 260),
        fill=(30, 30, 30),
        width=12,
    )

    draw.line(
        (cx + 50, cy + 60, cx + 80, cy + 260),
        fill=(30, 30, 30),
        width=12,
    )

    # Speech bubble
    bubble = (480, 210, 710, 330)

    draw.rounded_rectangle(
        bubble,
        radius=25,
        fill="white",
        outline=(25, 25, 25),
        width=5,
    )

    draw.text(
        (505, 235),
        "Let's go!",
        font=body_font,
        fill=(20, 20, 20),
    )

    draw.polygon(
        [(500, 330), (520, 350), (535, 325)],
        fill="white",
        outline=(25, 25, 25),
    )

    draw.text(
        (55, 680),
        f"Demo illustration • {art_style}",
        font=body_font,
        fill=(70, 70, 70),
    )

    image.save(path, format="PNG")