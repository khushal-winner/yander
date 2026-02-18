import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_post_auth_refresh_refresh_access_token_using_refresh_token():
    register_url = f"{BASE_URL}/auth/register"
    login_url = f"{BASE_URL}/auth/login"
    refresh_url = f"{BASE_URL}/auth/refresh"

    email = "testuser_refresh@example.com"
    password = "TestPassword123!"
    name = "Test User Refresh"

    register_data = None
    login_data = None

    try:
        # Register user
        register_payload = {
            "email": email,
            "password": password,
            "name": name
        }
        register_resp = requests.post(register_url, json=register_payload, timeout=TIMEOUT)
        assert register_resp.status_code == 201, f"User registration failed: {register_resp.text}"
        register_data = register_resp.json()
        refresh_token = register_data.get("refreshToken")
        assert isinstance(refresh_token, str) and len(refresh_token) > 0, "Refresh token missing on registration"

        # Login user
        login_payload = {
            "email": email,
            "password": password
        }
        login_resp = requests.post(login_url, json=login_payload, timeout=TIMEOUT)
        assert login_resp.status_code == 200, f"User login failed: {login_resp.text}"
        login_data = login_resp.json()
        refresh_token = login_data.get("refreshToken")
        assert isinstance(refresh_token, str) and len(refresh_token) > 0, "Refresh token missing on login"

        # Use refresh token to get new access token
        refresh_payload = {"refreshToken": refresh_token}
        refresh_resp = requests.post(refresh_url, json=refresh_payload, timeout=TIMEOUT)
        assert refresh_resp.status_code == 200, f"Refresh token request failed: {refresh_resp.text}"
        refresh_data = refresh_resp.json()
        new_access_token = refresh_data.get("accessToken")
        assert isinstance(new_access_token, str) and len(new_access_token) > 0, "New access token missing on refresh"
    finally:
        # Cleanup: delete user
        user_id = None
        if register_data and 'id' in register_data:
            user_id = register_data["id"]
        elif login_data and 'id' in login_data:
            user_id = login_data["id"]
        if user_id:
            delete_url = f"{BASE_URL}/users/{user_id}"
            try:
                del_resp = requests.delete(delete_url, timeout=TIMEOUT)
                assert del_resp.status_code in [204, 404]
            except Exception:
                pass

test_post_auth_refresh_refresh_access_token_using_refresh_token()
