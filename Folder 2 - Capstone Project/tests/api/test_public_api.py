"""
Standalone API test module — proves the framework isn't UI-only.
Reuses the same PyTest fixture pattern, config, and reporting setup
as the Selenium suite, just pointed at a public REST API instead
of a browser.

Target: https://jsonplaceholder.typicode.com/ (public fake REST API)
"""


def test_get_all_users(api_client):
    response = api_client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_get_single_user(api_client):
    response = api_client.get("/users/1")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert "email" in body


def test_create_user(api_client):
    payload = {"name": "Test User", "email": "testuser@example.com"}
    response = api_client.post("/users", payload=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == payload["name"]


def test_update_user(api_client):
    payload = {"name": "Updated Name"}
    response = api_client.put("/users/1", payload=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"


def test_delete_user(api_client):
    response = api_client.delete("/users/1")
    assert response.status_code == 200


def test_get_nonexistent_user_returns_404(api_client):
    response = api_client.get("/users/9999")
    assert response.status_code == 404
