from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_main():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "Hello"}

def test_read_item():
    resp = client.get("/items/item1", headers={"X-Token": "secrettoken"})
    assert resp.status_code == 200
    assert resp.json() == {
        "id": "1",
        "title": "item one",
        "desc": "item"
    }

def test_read_item_wrong_token():
    resp = client.get("/items/item1", headers={"X-Token": "wrong token"})
    assert resp.status_code == 400
    assert resp.json() == {"detail": "Invalid X-Token header."}

def test_read_non_exist_entry():
    resp = client.get("/items/item3", headers={"X-Token": "secrettoken"})
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Item not found."}


def test_create_item():
    resp = client.post(
        "/items/",
        headers={"X-Token": "secrettoken"},
        json={"id": "itemx", "title": "item x", "desc": "item"}
    )
    assert resp.status_code == 200
    assert resp.json() == {
        "id": "itemx",
        "title": "item x",
        "desc": "item"
    }

def test_create_item_wrong_token():
    resp = client.post(
        "/items/",
        headers={"X-Token": "wrong token"},
        json={"id": "itemy", "title": "item y", "desc": "item"}
    )
    assert resp.status_code == 400
    assert resp.json() == {"detail": "Invalid X-Token header."}

def test_create_exist_entry():
    resp = client.post(
        "/items/",
        headers={"X-Token": "secrettoken"},
        json={"id": "item1", "title": "item one", "desc": "item"}
    )
    assert resp.status_code == 400
    assert resp.json() == {"detail": "Item exists."}
