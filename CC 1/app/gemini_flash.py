from google import genai
from google.genai import types

from .config import get_settings
from .schemas import ComicOutline


def generate_outline(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str,
) -> list[dict]:

    settings = get_settings()

    # Demo Mode
    if settings.demo_mode or not settings.gemini_api_key:

        panels = [
            (
                "The Invitation",
                f"{character_name} discovers a mysterious clue in {setting}.",
            ),
            (
                "A Strange Path",
                f"{character_name} follows the clue deeper into {setting}.",
            ),
            (
                "The Challenge",
                f"{character_name} faces an unexpected challenge.",
            ),
            (
                "The Discovery",
                f"{character_name} learns the secret behind the adventure.",
            ),
            (
                "A New Beginning",
                f"{character_name} returns changed, carrying a hopeful lesson.",
            ),
        ]

        return [
            {
                "panel_number": index,
                "title": title,
                "scene_description": description,
                "image_prompt": (
                    f"Panel {index}, {art_style} comic illustration, "
                    f"{setting}, main character {character_name}, "
                    f"{description}. Consistent character appearance, "
                    "expressive poses, clean composition."
                ),
            }
            for index, (title, description) in enumerate(panels, start=1)
        ]

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    prompt = f"""
Create a cohesive {settings.panel_count}-panel comic outline.

Story idea:
{story_prompt}

Main character:
{character_name}

Setting:
{setting}

Tone:
{tone}

Art style:
{art_style}

Requirements:

- Exactly {settings.panel_count} panels.
- Each panel must have:
  panel_number
  title
  scene_description
  image_prompt
- Keep the main character visually consistent.
- Make the plot flow naturally from panel to panel.
- Image prompts must be visual descriptions.
- Do not put dialogue inside image prompts.
"""

    response = client.models.generate_content(
        model=settings.gemini_outline_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ComicOutline,
        ),
    )

    result = ComicOutline.model_validate_json(
        response.text
    )

    if len(result.panels) != settings.panel_count:
        raise ValueError(
            "Gemini returned an unexpected number of panels."
        )

    return [
        panel.model_dump()
        for panel in result.panels
    ]