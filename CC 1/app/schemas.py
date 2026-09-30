from typing import List

from pydantic import BaseModel, Field, field_validator


class PromptRequest(BaseModel):
    story_prompt: str = Field(..., min_length=5, max_length=1200)
    character_name: str = Field(..., min_length=1, max_length=80)
    setting: str = Field(..., min_length=1, max_length=120)
    tone: str = Field(..., min_length=1, max_length=50)
    art_style: str = Field(..., min_length=1, max_length=80)

    @field_validator("*")
    @classmethod
    def clean_text(cls, value: str) -> str:
        value = " ".join(value.strip().split())

        if not value:
            raise ValueError("Field cannot be empty.")

        return value


class PanelOutline(BaseModel):
    panel_number: int
    title: str
    scene_description: str
    image_prompt: str


class ComicOutline(BaseModel):
    panels: List[PanelOutline]


class PanelStory(BaseModel):
    panel_number: int
    title: str
    caption: str
    narration: str
    dialogue: str


class ComicStory(BaseModel):
    panels: List[PanelStory]


class ComicResponse(BaseModel):
    comic_id: str
    panels: list[dict]
    pdf_url: str