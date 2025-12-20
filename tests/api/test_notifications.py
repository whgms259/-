from fastapi.testclient import TestClient

def test_create_and_get_notifications(client: TestClient):
    """
    Test creating a user, then a notification for that user,
    retrieving it, and marking it as read.
    """
    # 1. Create a test user
    user_response = client.post(
        "/users/",
        json={"email": "notification.test@example.com", "username": "notificationuser", "password": "password"},
    )
    assert user_response.status_code == 200
    user_data = user_response.json()
    user_id = user_data["id"]

    # 2. Create a notification for the user
    notification_data = {"message": "Test notification", "user_id": user_id}
    notification_response = client.post("/notifications/", json=notification_data)
    assert notification_response.status_code == 200
    created_notification = notification_response.json()
    assert created_notification["message"] == "Test notification"
    assert created_notification["user_id"] == user_id
    assert not created_notification["read"]
    notification_id = created_notification["id"]

    # 3. Retrieve notifications for the user
    get_response = client.get(f"/users/{user_id}/notifications/")
    assert get_response.status_code == 200
    notifications = get_response.json()
    assert isinstance(notifications, list)
    assert len(notifications) == 1
    assert notifications[0]["id"] == notification_id

    # 4. Mark the notification as read
    patch_response = client.patch(f"/notifications/{notification_id}/read")
    assert patch_response.status_code == 200
    read_notification = patch_response.json()
    assert read_notification["read"]

    # 5. Verify the notification is marked as read
    get_response_after_read = client.get(f"/users/{user_id}/notifications/")
    assert get_response_after_read.status_code == 200
    notifications_after_read = get_response_after_read.json()
    assert notifications_after_read[0]["read"]