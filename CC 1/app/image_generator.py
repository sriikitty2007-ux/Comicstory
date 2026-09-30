from PIL import Image
from huggingface_hub import InferenceClient
from uuid import uuid4

from .config import get_settings
from .demo_data import make_demo_image


def generate_image(
    image_prompt: str,
    panel_number: int,
    title: str,
    art_style: str,
) -> str:

    settings = get_settings()

    filename = (
        f"{uuid4().hex}_panel_{panel_number}.png"
    )

    output_path = (
        settings.panels_dir / filename
    )

    # Demo Mode
    if settings.demo_mode or not settings.hf_token:

        make_demo_image(
            output_path,
            panel_number,
            title,
            art_style,
        )

        return f"/static/panels/{filename}"

    client = InferenceClient(
        provider=settings.hf_provider,
        api_key=settings.hf_token,
    )

    prompt = (
        f"{image_prompt}. "
        f"Style: {art_style}. "
        "Comic panel composition, expressive characters, "
        "cinematic lighting, clear focal point, "
        "no written text, no watermark."
    )

    image: Image.Image = client.text_to_image(
        prompt=prompt,
        model=settings.hf_image_model,
    )

    image.save(
        output_path,
        format="PNG",
    )

    return f"/static/panels/{filename}"