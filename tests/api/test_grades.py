from fastapi.testclient import TestClient
import random

def get_auth_token(client: TestClient, username: str, password: str):
    response = client.post(
        "/token",
        data={"username": username, "password": password}
    )
    return response.json()["access_token"]

def test_create_and_get_grade(client: TestClient):
    """
    Test creating a user, logging in, then creating a grade record for that user,
    and then retrieving grade records for that user using the access token.
    """
    random_id = random.randint(1000, 9999)
    test_email = f"grade_test_{random_id}@example.com"
    test_username = f"gradeuser_{random_id}"
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
    grade_response = client.post(
        "/grades/",
        json={"subject": "Math", "score": 95},
        headers=headers
    )
    if grade_response.status_code != 200:
        print(grade_response.json())
    assert grade_response.status_code == 200
    grade_data = grade_response.json()
    assert "id" in grade_data
    assert grade_data["subject"] == "Math"
    assert grade_data["score"] == 95
    assert "user_id" in grade_data

    # 4. Retrieve grade records for the user
    get_grades_response = client.get(f"/grades/me", headers=headers)
    assert get_grades_response.status_code == 200
    all_grades = get_grades_response.json()
    assert isinstance(all_grades, list)
    assert len(all_grades) == 1
    assert all_grades[0]["id"] == grade_data["id"]
    assert all_grades[0]["subject"] == "Math"
    assert all_grades[0]["score"] == 95

def test_get_average_grades(client: TestClient):
    """
    Test creating multiple grade records for a user and then retrieving their average grades.
    """
    random_id = random.randint(1000, 9999)
    test_email = f"average_grade_test_{random_id}@example.com"
    test_username = f"avggradeuser_{random_id}"
    test_password = "testpass"

    # 1. Create a test user
    client.post(
        "/users/",
        json={"email": test_email, "username": test_username, "password": test_password},
    )

    # 2. Login to get an access token
    access_token = get_auth_token(client, test_username, test_password)
    headers = {"Authorization": f"Bearer {access_token}"}

    # 3. Create multiple grade records
    client.post("/grades/", json={"subject": "Math", "score": 90}, headers=headers)
    client.post("/grades/", json={"subject": "Math", "score": 80}, headers=headers)
    client.post("/grades/", json={"subject": "Science", "score": 70}, headers=headers)
    client.post("/grades/", json={"subject": "Science", "score": 100}, headers=headers)
    client.post("/grades/", json={"subject": "English", "score": 75}, headers=headers)

    # 4. Retrieve average grades
    average_grades_response = client.get(f"/grades/me/average", headers=headers)
    assert average_grades_response.status_code == 200
    average_grades_data = average_grades_response.json()

    expected_averages = {
        "Math": 85.0,
        "Science": 85.0,
        "English": 75.0
    }
    assert average_grades_data == expected_averages

def test_get_average_grades_no_grades(client: TestClient):
    """
    Test retrieving average grades for a user who has no grade records.
    """
    random_id = random.randint(1000, 9999)
    test_email = f"no_grade_test_{random_id}@example.com"
    test_username = f"nogradeuser_{random_id}"
    test_password = "testpass"

    # 1. Create a test user
    client.post(
        "/users/",
        json={"email": test_email, "username": test_username, "password": test_password},
    )

    # 2. Login to get an access token
    access_token = get_auth_token(client, test_username, test_password)
    headers = {"Authorization": f"Bearer {access_token}"}

    # 3. Retrieve average grades (should be 404 as no grades exist)
    average_grades_response = client.get(f"/grades/me/average", headers=headers)
    assert average_grades_response.status_code == 404
    assert average_grades_response.json() == {"detail": "No grades found for the user."}