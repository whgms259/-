from fastapi.testclient import TestClient
import random
import pytest
import asyncio
import json

def get_auth_token(client: TestClient, username: str, password: str) -> str:
    response = client.post(
        "/token",
        data={"username": username, "password": password}
    )
    if response.status_code != 200:
        raise Exception(f"Failed to get auth token: {response.text}")
    return response.json()["access_token"]

@pytest.mark.asyncio
async def test_websocket_notifications(client: TestClient):
    """
    Test that a user receives a notification over WebSocket when one is created for them.
    """
    random_id = random.randint(1000, 9999)
    test_email = f"ws_test_{random_id}@example.com"
    test_username = f"wsuser_{random_id}"
    test_password = "testpass"

    # 1. Create a test user
    user_response = client.post(
        "/users/",
        json={"email": test_email, "username": test_username, "password": test_password},
    )
    assert user_response.status_code == 200

    # 2. Login to get an access token
    access_token = get_auth_token(client, test_username, test_password)

    # 3. Connect to the WebSocket endpoint
    with client.websocket_connect(f"/ws/notifications?token={access_token}") as websocket:
        # 4. In parallel, create a notification for the user via HTTP
        # Give the server a moment to establish the connection before sending the message
        await asyncio.sleep(0.1)
        
        notification_message = f"Hello {test_username}"
        response = client.post(
            "/notifications/",
            json={"message": notification_message},
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200
        
        # 5. Assert that the WebSocket received the new notification
        data = websocket.receive_text()
        received_data = json.loads(data)
        
        assert received_data["type"] == "new_notification"
        assert received_data["data"]["message"] == notification_message
        assert received_data["data"]["read"] is False

def test_websocket_invalid_token(client: TestClient):
    """
    Test that the WebSocket connection is rejected if the token is invalid.
    """
    with pytest.raises(Exception): # The client will raise an exception on a closed connection
        with client.websocket_connect("/ws/notifications?token=invalidtoken") as websocket:
            # The connection should be closed by the server, and the client will error out.
            websocket.receive_text()
