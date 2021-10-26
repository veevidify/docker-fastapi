from fastapi.testclient import TestClient

from .config import Settings
from .main import app, get_settings

client = TestClient(app)

def overrides_mock_settings():
    return Settings(app_key="mockkey", app_name="mock app")

app.dependency_overrides[get_settings] = overrides_mock_settings

def test_main():
    resp = client.get("/info")
    data = resp.json()

    assert data == {
        "app_name": "mock app",
        "app_key": "mockkey"
    }
