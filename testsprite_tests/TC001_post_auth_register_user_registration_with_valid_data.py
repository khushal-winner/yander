import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_post_auth_register_user_registration_with_valid_data():
    url = f"{BASE_URL}/auth/register"
    # Unique email to avoid duplicate error in case of rerun
    unique_email = f"test_user_{uuid.uuid4().hex[:8]}@example.com"
    payload = {
        "email": unique_email,
        "password": "StrongPassword123!",
        "name": "Test User"
    }
    headers = {"Content-Type": "application/json"}

    response = None
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
        assert response.status_code == 201, f"Expected 201 Created, got {response.status_code}"
        json_resp = response.json()
        # Check user object keys
        assert "user" in json_resp, "Response missing 'user'"
        user = json_resp["user"]
        assert isinstance(user, dict), "'user' is not a dict"
        assert "email" in user and user["email"] == unique_email, "User email mismatch"
        assert "id" in user, "User object missing 'id'"

        # Check tokens
        assert "accessToken" in json_resp, "Missing accessToken"
        assert isinstance(json_resp["accessToken"], str) and len(json_resp["accessToken"]) > 0, "Invalid accessToken"
        assert "refreshToken" in json_resp, "Missing refreshToken"
        assert isinstance(json_resp["refreshToken"], str) and len(json_resp["refreshToken"]) > 0, "Invalid refreshToken"
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"
    finally:
        # Cleanup: delete the created user by login + revoke or direct delete if possible
        # Since no delete user endpoint auth is defined and auth for DELETE /users/:id is false,
        # we can delete the user directly by id (from response user.id)
        if response and response.status_code == 201:
            user_id = json_resp["user"].get("id")
            if user_id:
                try:
                    del_url = f"{BASE_URL}/users/{user_id}"
                    del_response = requests.delete(del_url, timeout=TIMEOUT)
                    assert del_response.status_code == 204, f"User cleanup failed with status {del_response.status_code}"
                except requests.RequestException:
                    # Just pass - cleanup best effort
                    pass

test_post_auth_register_user_registration_with_valid_data()