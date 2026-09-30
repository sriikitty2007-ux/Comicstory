from typing import Any


COMICS: dict[str, dict[str, Any]] = {}


def save_comic(comic_id: str, comic: dict[str, Any]) -> None:
    COMICS[comic_id] = comic


def get_comic(comic_id: str) -> dict[str, Any] | None:
    return COMICS.get(comic_id)