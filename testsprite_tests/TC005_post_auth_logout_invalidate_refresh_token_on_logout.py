import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_post_auth_logout_invalidate_refresh_token_on_logout():
    # Test user credentials for auth login
    email = "test@test.com"
    password = "TestPassword123!"
    # Register the user first to ensure the user exists (if already registered it might fail but we continue)
    register_payload = {
        "email": email,
        "password": password,
        "name": "Test User"
    }
    try:
        requests.post(f"{BASE_URL}/auth/register", json=register_payload, timeout=TIMEOUT)
    except requests.exceptions.RequestException:
        pass  # If already registered, ignore

    # Login to get access token and refresh token
    login_payload = {
        "email": email,
        "password": password
    }
    login_resp = requests.post(f"{BASE_URL}/auth/login", json=login_payload, timeout=TIMEOUT)
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
    login_data = login_resp.json()
    access_token = login_data.get("accessToken")
    refresh_token = login_data.get("refreshToken")
    assert access_token is not None, "Missing access token in login response"
    assert refresh_token is not None, "Missing refresh token in login response"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Call POST /auth/logout with Authorization header and refreshToken in body
    logout_payload = {
        "refreshToken": refresh_token
    }
    logout_resp = requests.post(f"{BASE_URL}/auth/logout", headers=headers, json=logout_payload, timeout=TIMEOUT)
    assert logout_resp.status_code == 200, f"Logout failed: {logout_resp.text}"
    logout_json = logout_resp.json()
    # Expect some success message presence (check message key or similar)
    assert any(key in logout_json for key in ("message", "success", "msg")), "Success message missing in logout response"

    # Verify refresh token is invalidated by attempting to refresh token with that refresh token
    refresh_payload = {
        "refreshToken": refresh_token
    }
    refresh_resp = requests.post(f"{BASE_URL}/auth/refresh", json=refresh_payload, timeout=TIMEOUT)
    assert refresh_resp.status_code == 401, f"Refresh token was not invalidated after logout: {refresh_resp.text}"

test_post_auth_logout_invalidate_refresh_token_on_logout()