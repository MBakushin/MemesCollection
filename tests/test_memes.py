from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..main import app
from ..core.database import Base, get_db


SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db:5432/memes_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def test_client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client


def test_create_meme(test_client):
    response = test_client.post(
        "/memes/",
        data={"title": "Test Meme", "description": "Test Description"},
        files={"file": ("test_image.png", b"file_content", "image/png")},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Meme"


def test_read_memes(test_client):
    response = test_client.get("/memes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_meme(test_client):
    response = test_client.post(
        "/memes/",
        data={"title": "Another Test Meme", "description": "Another Description"},
        files={"file": ("another_test_image.png", b"file_content", "image/png")},
    )
    meme_id = response.json()["id"]
    response = test_client.get(f"/memes/{meme_id}")
    assert response.status_code == 200
    assert response.json()["id"] == meme_id


def test_update_meme(test_client):
    response = test_client.post(
        "/memes/",
        data={"title": "Update Test Meme", "description": "Update Description"},
        files={"file": ("update_test_image.png", b"file_content", "image/png")},
    )
    meme_id = response.json()["id"]
    update_data = {"title": "Updated Title", "description": "Updated Description"}
    response = test_client.put(f"/memes/{meme_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"


def test_delete_meme(test_client):
    response = test_client.post(
        "/memes/",
        data={"title": "Delete Test Meme", "description": "Delete Description"},
        files={"file": ("delete_test_image.png", b"file_content", "image/png")},
    )
    meme_id = response.json()["id"]
    response = test_client.delete(f"/memes/{meme_id}")
    assert response.status_code == 200
    response = test_client.get(f"/memes/{meme_id}")
    assert response.status_code == 404
