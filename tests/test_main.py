from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Notes App is running!"}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_note():
    response = client.post("/notes", json={"title": "Test", "content": "Hello"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test"


def test_get_notes():
    response = client.get("/notes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_note():
    create = client.post("/notes", json={"title": "Note A", "content": "Content A"})
    note_id = create.json()["id"]
    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Note A"


def test_get_note_not_found():
    response = client.get("/notes/99999")
    assert response.status_code == 404


def test_delete_note():
    create = client.post("/notes", json={"title": "Delete Me", "content": "Bye"})
    note_id = create.json()["id"]
    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 200


def test_delete_note_not_found():
    response = client.delete("/notes/99999")
    assert response.status_code == 404