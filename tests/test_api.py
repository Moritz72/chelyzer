from fastapi.testclient import TestClient

from chelyzer_api.app import create_app


def test_api() -> None:
    """Test API initialization."""
    app = create_app()
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 404
