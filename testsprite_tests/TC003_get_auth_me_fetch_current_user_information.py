import requests

BASE_URL = "http://localhost:8000"
REGISTER_ENDPOINT = "/auth/register"
LOGIN_ENDPOINT = "/auth/login"
AUTH_ME_ENDPOINT = "/auth/me"
TIMEOUT = 30

def test_get_auth_me_fetch_current_user_information():
    # User credentials for registration and login
    user_data = {
        "email": "test@test.com",
        "password": "TestPassword123!",
        "name": "Test User"
    }

    access_token = None
    refresh_token = None

    try:
        # Register user
        reg_resp = requests.post(
            BASE_URL + REGISTER_ENDPOINT,
            json=user_data,
            timeout=TIMEOUT
        )
        if reg_resp.status_code != 201 and reg_resp.status_code != 400:
            reg_resp.raise_for_status()
        # If user already registered (400), continue to login

        # Login user
        login_resp = requests.post(
            BASE_URL + LOGIN_ENDPOINT,
            json={"email": user_data["email"], "password": user_data["password"]},
            timeout=TIMEOUT
        )
        assert login_resp.status_code == 200, f"Login failed with status {login_resp.status_code}: {login_resp.text}"
        login_data = login_resp.json()
        assert "accessToken" in login_data and isinstance(login_data["accessToken"], str)
        assert "refreshToken" in login_data and isinstance(login_data["refreshToken"], str)
        access_token = login_data["accessToken"]
        refresh_token = login_data["refreshToken"]

        # Get current user info using access token
        headers = {"Authorization": f"Bearer {access_token}"}
        auth_me_resp = requests.get(
            BASE_URL + AUTH_ME_ENDPOINT,
            headers=headers,
            timeout=TIMEOUT
        )
        assert auth_me_resp.status_code == 200, f"GET /auth/me failed with status {auth_me_resp.status_code}: {auth_me_resp.text}"
        user_obj = auth_me_resp.json()
        assert isinstance(user_obj, dict), "Response is not a JSON object"
        # Basic checks on user object
        assert "email" in user_obj and user_obj["email"] == user_data["email"]
        assert "name" in user_obj and user_obj["name"] == user_data["name"]
        assert "id" in user_obj and isinstance(user_obj["id"], (int, str))

    finally:
        # Cleanup: If registered via this test (not guaranteed), try to delete the user by logging in and calling DELETE user API if available
        # There is no DELETE user endpoint auth_required false in PRD, so skip actual deletion to avoid accidental removal
        pass

test_get_auth_me_fetch_current_user_information()