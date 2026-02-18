import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_post_auth_register_user_registration_with_valid_data():
    url = f"{BASE_URL}/auth/register"
    unique_email = f"testuser_{uuid.uuid4().hex}@example.com"
    payload = {
        "email": unique_email,
        "password": "StrongP@ssw0rd",
        "name": "Test User"
    }
    headers = {
        "Content-Type": "application/json"
    }

    user_id = None  # To track the created user for cleanup if possible

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()

        # Validate user object presence
        assert "user" in data, "Response JSON missing 'user' key"
        user = data["user"]
        assert isinstance(user, dict), "'user' should be an object"
        assert "id" in user, "'user' object missing 'id'"
        user_id = user["id"]

        # Validate required fields in user object
        assert user.get("email") == unique_email, "User email mismatch"
        assert "name" in user, "User 'name' missing"

        # Validate tokens presence
        assert "accessToken" in data, "accessToken missing from response"
        assert "refreshToken" in data, "refreshToken missing from response"
        assert isinstance(data["accessToken"], str) and len(data["accessToken"]) > 0, "Invalid accessToken"
        assert isinstance(data["refreshToken"], str) and len(data["refreshToken"]) > 0, "Invalid refreshToken"

    except requests.RequestException as e:
        assert False, f"HTTP request failed: {str(e)}"

    finally:
        # Clean up: delete the created user if possible (no auth required)
        # According to PRD, DELETE /users/:id has no auth requirement
        if user_id:
            try:
                del_url = f"{BASE_URL}/users/{user_id}"
                del_response = requests.delete(del_url, timeout=TIMEOUT)
                # Accept 204 No Content or 404 User not found (if already deleted)
                assert del_response.status_code in (204, 404), f"Cleanup delete failed with status {del_response.status_code}"
            except requests.RequestException:
                pass

test_post_auth_register_user_registration_with_valid_data()