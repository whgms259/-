from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone
import random

def get_auth_token(client: TestClient, username: str, password: str):
    response = client.post(
        "/token",
        data={"username": username, "password": password}
    )
    return response.json()["access_token"]

def test_create_and_get_attendance(client: TestClient):
    """
    Test creating a user, logging in, then creating an attendance record for that user,
    and then retrieving attendance records for that user using the access token.
    """
    random_id = random.randint(1000, 9999)
    test_email = f"attendance_test_{random_id}@example.com"
    test_username = f"attenduser_{random_id}"
    test_password = "testpass"

    # 1. Create a test user
    client.post(
        "/users/",
        json={"email": test_email, "username": test_username, "password": test_password},
    )

    # 2. Login to get an access token
    access_token = get_auth_token(client, test_username, test_password)
    headers = {"Authorization": f"Bearer {access_token}"}

    # 3. Create an attendance record (check-in)
    check_in_time = datetime.now(timezone.utc).isoformat()
    attendance_response = client.post(
        "/attendances/",
        json={"check_in_time": check_in_time},
        headers=headers
    )
    if attendance_response.status_code != 200:
        print(attendance_response.json())
    assert attendance_response.status_code == 200
    attendance_data = attendance_response.json()
    assert "id" in attendance_data
    assert "check_in_time" in attendance_data
    assert attendance_data["check_out_time"] is None
    assert "user_id" in attendance_data

    # 4. Retrieve attendance records for the user
    get_attendance_response = client.get(f"/attendances/me", headers=headers)
    assert get_attendance_response.status_code == 200
    all_attendances = get_attendance_response.json()
    assert isinstance(all_attendances, list)
    assert len(all_attendances) == 1
    assert all_attendances[0]["id"] == attendance_data["id"]

    # 5. Try to create another attendance for the same user (just a check-in)
    check_in_time_2 = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    attendance_response_2 = client.post(
        "/attendances/",
        json={"check_in_time": check_in_time_2},
        headers=headers
    )
    assert attendance_response_2.status_code == 200

    # 6. Retrieve again to confirm two records
    get_attendance_response_2 = client.get(f"/attendances/me", headers=headers)
    assert get_attendance_response_2.status_code == 200
    all_attendances_2 = get_attendance_response_2.json()
    assert len(all_attendances_2) == 2