from fastapi.testclient import TestClient
import random

def test_create_user(client: TestClient):
    """
    Test creating a user via the API.
    """
    random_id = random.randint(1000, 9999)
    test_email = f"test_{random_id}@example.com"
    test_username = f"testuser_{random_id}"
    response = client.post(
        "/users/",
        json={"email": test_email, "username": test_username, "password": "testpass"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_email
    assert data["username"] == test_username
    assert "id" in data

def test_login_for_access_token(client: TestClient):
    """
    Test user login and access token retrieval.
    """
    random_id = random.randint(1000, 9999)
    test_email = f"login_{random_id}@example.com"
    test_username = f"loginuser_{random_id}"
    test_password = "testpass"

    # Create a user first
    client.post(
        "/users/",
        json={"email": test_email, "username": test_username, "password": test_password},
    )

    # Then try to login
    response = client.post(
        "/token",
        data={"username": test_username, "password": test_password},
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert "token_type" in token_data
    assert token_data["token_type"] == "bearer"