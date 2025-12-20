from fastapi.testclient import TestClient
import random

def get_auth_token(client: TestClient, username: str, password: str):
    response = client.post(
        "/token",
        data={"username": username, "password": password}
    )
    return response.json()["access_token"]

def test_create_and_get_grades(client: TestClient):
    """
    Test creating a user, logging in, then creating grade records for that user,
    and then retrieving grade records for that user using the access token.
    """
    random_id = random.randint(1000, 9999)
    test_email = f"grades_test_{random_id}@example.com"
    test_username = f"gradesuser_{random_id}"
    test_password = "testpass"

    # 1. Create a test user
    client.post(
        "/users/",
        json={"email": test_email, "username": test_username, "password": test_password},
    )

    # 2. Login to get an access token
    access_token = get_auth_token(client, test_username, test_password)
    headers = {"Authorization": f"Bearer {access_token}"}

    # 3. Create a grade record
    grade_data_1 = {"subject": "Math", "score": 95}
    grade_response_1 = client.post("/grades/", json=grade_data_1, headers=headers)
    
    assert grade_response_1.status_code == 200
    created_grade_1 = grade_response_1.json()
    assert created_grade_1["subject"] == grade_data_1["subject"]
    assert created_grade_1["score"] == grade_data_1["score"]
    assert "id" in created_grade_1
    assert "user_id" in created_grade_1 # user_id should be present in the response model

    # 4. Create a second grade record
    grade_data_2 = {"subject": "Science", "score": 88}
    grade_response_2 = client.post("/grades/", json=grade_data_2, headers=headers)
    assert grade_response_2.status_code == 200

    # 5. Retrieve all grades for the user
    get_grades_response = client.get(f"/grades/me", headers=headers)
    assert get_grades_response.status_code == 200
    all_grades = get_grades_response.json()
    
    assert isinstance(all_grades, list)
    assert len(all_grades) == 2
    
    subjects = {grade["subject"] for grade in all_grades}
    assert "Math" in subjects
    assert "Science" in subjects

def test_create_grade_unauthorized(client: TestClient):
    """
    Test creating a grade without authentication.
    """
    grade_data = {"subject": "History", "score": 75}
    response = client.post("/grades/", json=grade_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
