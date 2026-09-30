from google import genai
from google.genai import types

from .config import get_settings
from .schemas import ComicStory


def generate_story(
    outline: list[dict],
    character_name: str,
    tone: str,
) -> list[dict]:

    settings = get_settings()

    # Demo Mode
    if settings.demo_mode or not settings.gemini_api_key:

        return [
            {
                "panel_number": panel["panel_number"],
                "title": panel["title"],
                "caption": "The adventure continues...",
                "narration": (
                    f"{character_name} takes a brave step forward. "
                    f"The {tone} atmosphere makes every moment feel important."
                ),
                "dialogue": (
                    f"{character_name}: "
                    "I have to find out what this means!"
                ),
            }
            for panel in outline
        ]

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    prompt = f"""
Expand this outline into a polished comic script.

Main character:
{character_name}

Tone:
{tone}

Outline:
{outline}

Return exactly one story object containing
one panel entry for every outline panel.

For each panel provide:

panel_number
title
caption
narration
dialogue

Keep the plot coherent and do not add extra panels.
"""

    response = client.models.generate_content(
        model=settings.gemini_story_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ComicStory,
        ),
    )

    result = ComicStory.model_validate_json(
        response.text
    )

    return [
        panel.model_dump()
        for panel in result.panels
    ]