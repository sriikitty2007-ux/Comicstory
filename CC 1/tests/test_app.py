import os

os.environ["DEMO_MODE"] = "true"


from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_homepage():

    response = client.get("/")

    assert response.status_code == 200

    assert "ComicCraft" in response.text


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


def test_generate_json():

    payload = {
        "story_prompt": (
            "A brave fox explores "
            "an enchanted forest."
        ),
        "character_name": "Ari",
        "setting": "Enchanted forest",
        "tone": "funny",
        "art_style": "comic book",
    }

    response = client.post(
        "/generate-comic/json",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["layout"]) == 5

    assert data["pdf_url"].endswith(".pdf")


def test_missing_comic():

    response = client.get(
        "/download/not-a-real-id"
    )

    assert response.status_code == 404