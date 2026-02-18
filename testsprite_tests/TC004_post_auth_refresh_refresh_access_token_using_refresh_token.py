import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

HEADERS = {"Content-Type": "application/json"}

def test_post_auth_refresh():
    # Step 1: Login to get a valid refresh token
    login_payload = {
        "email": "test@test.com",
        "password": "testPassword123!"
    }
    login_resp = requests.post(
        f"{BASE_URL}/auth/login",
        json=login_payload,
        headers=HEADERS,
        timeout=TIMEOUT
    )
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
    login_data = login_resp.json()
    assert "refreshToken" in login_data, "No refreshToken returned on login"
    refresh_token = login_data["refreshToken"]

    # Step 2: Use the refresh token to get a new access token
    refresh_payload = {"refreshToken": refresh_token}
    refresh_resp = requests.post(
        f"{BASE_URL}/auth/refresh",
        json=refresh_payload,
        headers=HEADERS,
        timeout=TIMEOUT
    )

    assert refresh_resp.status_code == 200, f"Refresh token request failed: {refresh_resp.text}"
    refresh_data = refresh_resp.json()
    assert "accessToken" in refresh_data, "No accessToken returned on refresh"


test_post_auth_refresh()
