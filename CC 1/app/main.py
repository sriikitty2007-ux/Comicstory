from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .routes import router


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):

    settings.panels_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    settings.exports_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    yield


app = FastAPI(
    title="ComicCraft API",
    description=(
        "AI Comic Story Creator using "
        "Gemini and Hugging Face."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


app.mount(
    "/static",
    StaticFiles(
        directory=str(
            settings.static_dir
        )
    ),
    name="static",
)


app.include_router(router)