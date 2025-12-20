from fastapi.testclient import TestClient
import random

def get_auth_token(client: TestClient, username: str, password: str):
    response = client.post(
        "/token",
        data={"username": username, "password": password}
    )
    return response.json()["access_token"]

def test_create_and_get_notifications(client: TestClient):
    """
    Test creating a user, logging in, then creating a notification for that user,
    retrieving it, and marking it as read using the access token.
    """
    random_id = random.randint(1000, 9999)
    test_email = f"notification_test_{random_id}@example.com"
    test_username = f"notificationuser_{random_id}"
    test_password = "testpass"

    # 1. Create a test user
    client.post(
        "/users/",
        json={"email": test_email, "username": test_username, "password": test_password},
    )

    # 2. Login to get an access token
    access_token = get_auth_token(client, test_username, test_password)
    headers = {"Authorization": f"Bearer {access_token}"}

    # 3. Create a notification for the user
    notification_data = {"message": "Test notification"}
    notification_response = client.post("/notifications/", json=notification_data, headers=headers)
    assert notification_response.status_code == 200
    created_notification = notification_response.json()
    assert created_notification["message"] == "Test notification"
    assert created_notification["user_id"] is not None # User ID should be set by the server
    assert not created_notification["read"]
    notification_id = created_notification["id"]

    # 4. Retrieve notifications for the user
    get_response = client.get(f"/notifications/me", headers=headers)
    assert get_response.status_code == 200
    notifications = get_response.json()
    assert isinstance(notifications, list)
    assert len(notifications) == 1
    assert notifications[0]["id"] == notification_id

    # 5. Mark the notification as read
    patch_response = client.patch(f"/notifications/{notification_id}/read", headers=headers)
    assert patch_response.status_code == 200
    read_notification = patch_response.json()
    assert read_notification["read"]

    # 6. Verify the notification is marked as read
    get_response_after_read = client.get(f"/notifications/me", headers=headers)
    assert get_response_after_read.status_code == 200
    notifications_after_read = get_response_after_read.json()
    assert notifications_after_read[0]["read"]

def test_create_notification_unauthorized(client: TestClient):
    """
    Test creating a notification without authentication.
    """
    notification_data = {"message": "Unauthorized notification"}
    response = client.post("/notifications/", json=notification_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_notifications_unauthorized(client: TestClient):
    """
    Test getting notifications without authentication.
    """
    response = client.get("/notifications/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_mark_notification_as_read_unauthorized(client: TestClient):
    """
    Test marking a notification as read without authentication.
    """
    response = client.patch("/notifications/9999/read")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"