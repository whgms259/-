from fastapi.testclient import TestClient

def test_create_and_get_grades(client: TestClient):
    """
    Test creating a user, then creating a grade record for that user,
    and then retrieving grade records for that user.
    """
    # 1. Create a test user
    user_response = client.post(
        "/users/",
        json={"email": "grades.test@example.com", "username": "gradesuser", "password": "password"},
    )
    assert user_response.status_code == 200
    user_data = user_response.json()
    user_id = user_data["id"]

    # 2. Create a grade record
    grade_data_1 = {"subject": "Math", "score": 95, "user_id": user_id}
    grade_response_1 = client.post("/grades/", json=grade_data_1)
    
    assert grade_response_1.status_code == 200
    created_grade_1 = grade_response_1.json()
    assert created_grade_1["subject"] == grade_data_1["subject"]
    assert created_grade_1["score"] == grade_data_1["score"]
    assert created_grade_1["user_id"] == user_id
    assert "id" in created_grade_1

    # 3. Create a second grade record
    grade_data_2 = {"subject": "Science", "score": 88, "user_id": user_id}
    grade_response_2 = client.post("/grades/", json=grade_data_2)
    assert grade_response_2.status_code == 200

    # 4. Retrieve all grades for the user
    get_grades_response = client.get(f"/users/{user_id}/grades/")
    assert get_grades_response.status_code == 200
    all_grades = get_grades_response.json()
    
    assert isinstance(all_grades, list)
    assert len(all_grades) == 2
    
    subjects = {grade["subject"] for grade in all_grades}
    assert "Math" in subjects
    assert "Science" in subjects

def test_create_grade_for_nonexistent_user(client: TestClient):
    """
    Test creating a grade for a user that does not exist.
    """
    grade_data = {"subject": "History", "score": 75, "user_id": 999999}
    response = client.post("/grades/", json=grade_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
