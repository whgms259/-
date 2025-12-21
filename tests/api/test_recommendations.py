from fastapi.testclient import TestClient
import random

def get_auth_token(client: TestClient, username: str, password: str) -> str:
    response = client.post(
        "/token",
        data={"username": username, "password": password}
    )
    if response.status_code != 200:
        raise Exception(f"Failed to get auth token: {response.text}")
    return response.json()["access_token"]

def test_get_recommendations(client: TestClient):
    """
    Test creating a user, adding grades, and getting AI-based recommendations.
    """
    random_id = random.randint(1000, 9999)
    test_email = f"rec_test_{random_id}@example.com"
    test_username = f"recuser_{random_id}"
    test_password = "testpass"

    # 1. Create a test user
    user_response = client.post(
        "/users/",
        json={"email": test_email, "username": test_username, "password": test_password},
    )
    assert user_response.status_code == 200

    # 2. Login to get an access token
    access_token = get_auth_token(client, test_username, test_password)
    headers = {"Authorization": f"Bearer {access_token}"}

    # 3. Create grade records for the user
    # High score - should not be recommended
    client.post("/grades/", json={"subject": "Math", "score": 95}, headers=headers)
    # Low score - should be recommended
    client.post("/grades/", json={"subject": "History", "score": 70}, headers=headers)
    # Edge case score - should not be recommended
    client.post("/grades/", json={"subject": "Science", "score": 80}, headers=headers)

    # 4. Get recommendations
    rec_response = client.get("/users/me/recommendations", headers=headers)
    assert rec_response.status_code == 200
    
    recommendations = rec_response.json()
    assert isinstance(recommendations, list)
    assert len(recommendations) == 1
    
    recommendation = recommendations[0]
    assert recommendation["subject"] == "History"
    assert "Score is below 80" in recommendation["reason"]

def test_get_recommendations_no_low_scores(client: TestClient):
    """
    Test getting recommendations when user has no low scores.
    """
    random_id = random.randint(1000, 9999)
    test_email = f"rec_test_good_{random_id}@example.com"
    test_username = f"recusergood_{random_id}"
    test_password = "testpass"

    # 1. Create user and login
    client.post(
        "/users/",
        json={"email": test_email, "username": test_username, "password": test_password},
    )
    access_token = get_auth_token(client, test_username, test_password)
    headers = {"Authorization": f"Bearer {access_token}"}

    # 2. Create only high-score grade records
    client.post("/grades/", json={"subject": "Art", "score": 100}, headers=headers)
    client.post("/grades/", json={"subject": "Music", "score": 98}, headers=headers)

    # 3. Get recommendations
    rec_response = client.get("/users/me/recommendations", headers=headers)
    assert rec_response.status_code == 200
    recommendations = rec_response.json()
    assert isinstance(recommendations, list)
    assert len(recommendations) == 0

def test_get_recommendations_unauthorized(client: TestClient):
    """
    Test getting recommendations without authentication.
    """
    response = client.get("/users/me/recommendations")
    assert response.status_code == 401
