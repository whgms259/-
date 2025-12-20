from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone

def test_create_and_get_attendance(client: TestClient):
    """
    Test creating a user, then creating an attendance record for that user,
    and then retrieving attendance records for that user.
    """
    # 1. Create a test user
    user_response = client.post(
        "/users/",
        json={"email": "attendance@example.com", "username": "attenduser", "password": "password"},
    )
    assert user_response.status_code == 200
    user_data = user_response.json()
    user_id = user_data["id"]

    # 2. Create an attendance record (check-in)
    check_in_time = datetime.now(timezone.utc)
    attendance_response = client.post(
        "/attendances/",
        json={"user_id": user_id, "check_in_time": check_in_time.isoformat()},
    )
    assert attendance_response.status_code == 200
    attendance_data = attendance_response.json()
    assert attendance_data["user_id"] == user_id
    assert "id" in attendance_data
    assert "check_in_time" in attendance_data
    assert attendance_data["check_out_time"] is None

    # 3. Retrieve attendance records for the user
    get_attendance_response = client.get(f"/users/{user_id}/attendances/")
    assert get_attendance_response.status_code == 200
    all_attendances = get_attendance_response.json()
    assert isinstance(all_attendances, list)
    assert len(all_attendances) == 1
    assert all_attendances[0]["id"] == attendance_data["id"]
    assert all_attendances[0]["user_id"] == user_id

    # 4. Try to create another attendance for the same user (just a check-in)
    # This scenario might need more complex logic in the service (e.g., check for open attendance)
    # For now, we just ensure it creates a new one.
    check_in_time_2 = datetime.now(timezone.utc) + timedelta(hours=1)
    attendance_response_2 = client.post(
        "/attendances/",
        json={"user_id": user_id, "check_in_time": check_in_time_2.isoformat()},
    )
    assert attendance_response_2.status_code == 200
    assert attendance_response_2.json()["user_id"] == user_id

    # 5. Retrieve again to confirm two records
    get_attendance_response_2 = client.get(f"/users/{user_id}/attendances/")
    assert get_attendance_response_2.status_code == 200
    all_attendances_2 = get_attendance_response_2.json()
    assert len(all_attendances_2) == 2