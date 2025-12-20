import random
from locust import HttpUser, task, between

class StudentUser(HttpUser):
    wait_time = between(1, 5)
    
    def on_start(self):
        """On start, create a user and save the user_id."""
        self.user_id = None
        self.create_user()

    def create_user(self):
        random_username = f"locust_user_{random.randint(1, 100000)}"
        random_email = f"{random_username}@example.com"
        
        response = self.client.post("/users/", json={
            "email": random_email,
            "username": random_username,
            "password": "password"
        })
        
        if response.status_code == 200:
            self.user_id = response.json()["id"]
        elif response.status_code == 400 and "already registered" in response.text:
            # This is a simple way to handle existing users in a test environment.
            # In a real-world scenario, you might want to log in instead.
            # For this test, we'll just try to create another user.
            self.create_user() # Recursive call to retry with a new random user

    @task(5)
    def get_user_data(self):
        if self.user_id:
            self.client.get(f"/users/{self.user_id}/grades/")
            self.client.get(f"/users/{self.user_id}/attendances/")
            self.client.get(f"/users/{self.user_id}/notifications/")

    @task(2)
    def create_grade(self):
        if self.user_id:
            self.client.post("/grades/", json={
                "subject": "Math",
                "score": random.randint(50, 100),
                "user_id": self.user_id
            })

    @task(1)
    def create_notification(self):
        if self.user_id:
            self.client.post("/notifications/", json={
                "message": "This is a test notification from Locust.",
                "user_id": self.user_id
            })
