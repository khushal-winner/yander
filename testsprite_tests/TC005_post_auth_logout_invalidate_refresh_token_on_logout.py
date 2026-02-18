import requests

BASE_URL = "http://localhost:8000"
REGISTER_URL = f"{BASE_URL}/auth/register"
LOGIN_URL = f"{BASE_URL}/auth/login"
LOGOUT_URL = f"{BASE_URL}/auth/logout"
REFRESH_URL = f"{BASE_URL}/auth/refresh"

def test_post_auth_logout_invalidate_refresh_token():
    # Test user credentials
    email = "test@test.com"
    password = "TestPass123!"
    name = "Test User"

    # Register user (if exists might fail but still continue to login)
    reg_payload = {"email": email, "password": password, "name": name}
    try:
        reg_resp = requests.post(REGISTER_URL, json=reg_payload, timeout=30)
        if reg_resp.status_code not in (201, 400):
            reg_resp.raise_for_status()
    except requests.RequestException as e:
        raise AssertionError(f"User registration request failed: {e}")

    # Login user
    login_payload = {"email": email, "password": password}
    try:
        login_resp = requests.post(LOGIN_URL, json=login_payload, timeout=30)
        login_resp.raise_for_status()
        login_data = login_resp.json()
        access_token = login_data.get("accessToken")
        refresh_token = login_data.get("refreshToken")
        assert access_token and refresh_token, "Login response missing tokens"
    except requests.RequestException as e:
        raise AssertionError(f"User login request failed: {e}")

    # Prepare headers and payload for logout
    headers = {"Authorization": f"Bearer {access_token}"}
    logout_payload = {"refreshToken": refresh_token}

    # Perform logout to invalidate refresh token
    try:
        logout_resp = requests.post(LOGOUT_URL, headers=headers, json=logout_payload, timeout=30)
        assert logout_resp.status_code == 200, f"Logout status code expected 200 but got {logout_resp.status_code}"
        logout_json = logout_resp.json()
        assert "success" in logout_json.get("message", "").lower() or logout_json.get("message","").strip() != "", "Logout success message missing"
    except requests.RequestException as e:
        raise AssertionError(f"Logout request failed: {e}")

    # Attempt to refresh token after logout - token should be invalidated
    try:
        refresh_resp = requests.post(REFRESH_URL, json={"refreshToken": refresh_token}, timeout=30)
        assert refresh_resp.status_code == 401, f"Expected 401 after logout when refreshing with invalidated token but got {refresh_resp.status_code}"
    except requests.RequestException as e:
        # Some servers might respond with JSON error or just status code
        if hasattr(e.response, "status_code") and e.response.status_code == 401:
            pass
        else:
            raise AssertionError(f"Refresh token request after logout failed unexpectedly: {e}")

test_post_auth_logout_invalidate_refresh_token()