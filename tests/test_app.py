import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_shorten_valid_url(client):
    response = client.post("/api/shorten", json={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.get_json()
    assert "short_code" in data
    assert "short_url" in data

def test_shorten_invalid_url(client):
    response = client.post("/api/shorten", json={"url": "invalid-url"})
    assert response.status_code == 400

def test_redirect_and_click_count(client):
    shorten = client.post("/api/shorten", json={"url": "https://example.com"}).get_json()
    code = shorten["short_code"]
    for _ in range(3):
        res = client.get(f"/{code}")
        assert res.status_code == 302  # Redirect
    stats = client.get(f"/api/stats/{code}").get_json()
    assert stats["clicks"] == 3

def test_stats_for_invalid_code(client):
    response = client.get("/api/stats/unknown")
    assert response.status_code == 404

def test_redirect_invalid_code(client):
    response = client.get("/invalidcode")
    assert response.status_code == 404
