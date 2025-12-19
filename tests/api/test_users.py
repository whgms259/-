from fastapi.testclient import TestClient

def test_create_user(client: TestClient):
    """
    Test creating a user via the API.
    """
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "username": "testuser", "password": "password"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data
