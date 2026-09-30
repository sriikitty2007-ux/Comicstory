from uuid import uuid4

from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request,
)

from fastapi.responses import (
    FileResponse,
)

from fastapi.templating import Jinja2Templates

from .config import get_settings
from .schemas import PromptRequest
from .storage import (
    get_comic,
    save_comic,
)
from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_image
from .layout_builder import build_comic_layout
from .exporters import save_pdf


router = APIRouter()

settings = get_settings()

templates = Jinja2Templates(
    directory=str(settings.templates_dir)
)


def create_comic(
    request_data: PromptRequest,
) -> tuple[str, dict]:

    comic_id = uuid4().hex

    # Step 1: Generate outline
    outline = generate_outline(
        request_data.story_prompt,
        request_data.character_name,
        request_data.setting,
        request_data.tone,
        request_data.art_style,
    )

    # Step 2: Generate narration/dialogue
    story = generate_story(
        outline,
        request_data.character_name,
        request_data.tone,
    )

    # Step 3: Generate images
    images = []

    for panel in outline:

        image_path = generate_image(
            panel["image_prompt"],
            panel["panel_number"],
            panel["title"],
            request_data.art_style,
        )

        images.append(image_path)

    # Step 4: Build final layout
    layout = build_comic_layout(
        outline,
        story,
        images,
    )

    # Step 5: Export PDF
    pdf_url = save_pdf(
        layout,
        comic_id,
    )

    comic = {
        "comic_id": comic_id,
        "input": request_data.model_dump(),
        "layout": layout,
        "pdf_url": pdf_url,
    }

    save_comic(
        comic_id,
        comic,
    )

    return comic_id, comic


@router.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "demo_mode": settings.demo_mode,
        },
    )


@router.post("/generate")
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):

    try:

        data = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )

        comic_id, comic = create_comic(data)

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "comic": comic,
                "demo_mode": settings.demo_mode,
            },
        )

    except Exception as exc:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": (
                    f"Comic generation failed: {exc}"
                ),
                "demo_mode": settings.demo_mode,
            },
            status_code=500,
        )


@router.post("/generate-comic/json")
async def generate_json(
    payload: PromptRequest,
):

    try:

        _, comic = create_comic(
            payload
        )

        return comic

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.post("/test-image")
async def test_image(
    prompt: str = Form(...),
    art_style: str = Form("comic book"),
):

    try:

        path = generate_image(
            prompt,
            0,
            "Image Test",
            art_style,
        )

        return {
            "image_url": path
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.get("/download/{comic_id}")
async def download(
    comic_id: str,
):

    comic = get_comic(
        comic_id
    )

    if not comic:

        raise HTTPException(
            status_code=404,
            detail="Comic not found.",
        )

    pdf_file = (
        settings.static_dir
        / comic["pdf_url"]
        .removeprefix("/static/")
    )

    if not pdf_file.exists():

        raise HTTPException(
            status_code=404,
            detail="PDF file not found.",
        )

    return FileResponse(
        path=pdf_file,
        media_type="application/pdf",
        filename=pdf_file.name,
    )


@router.get("/export-success")
async def export_success(
    request: Request,
    comic_id: str | None = None,
):

    comic = (
        get_comic(comic_id)
        if comic_id
        else None
    )

    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={
            "comic": comic
        },
    )


@router.get("/health")
async def health():

    return {
        "status": "ok",
        "demo_mode": settings.demo_mode,
        "gemini_configured": bool(
            settings.gemini_api_key
        ),
        "huggingface_configured": bool(
            settings.hf_token
        ),
    }