import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_auth_login_returns_tokens_successfully():
    # First, register a user
    register_url = f"{BASE_URL}/auth/register"
    register_payload = {
        "email": "loginuser+tc009@example.com",
        "password": "password123",
        "name": "Login User TC009"
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        register_response = requests.post(register_url, json=register_payload, headers=headers, timeout=TIMEOUT)
        assert register_response.status_code == 201, f"Registration failed with status {register_response.status_code}"
    except requests.RequestException as e:
        assert False, f"Registration request failed: {e}"

    # Now test login
    login_url = f"{BASE_URL}/auth/login"
    login_payload = {
        "email": "loginuser+tc009@example.com",
        "password": "password123"
    }

    try:
        response = requests.post(login_url, json=login_payload, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Login request failed: {e}"

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    # Validate response structure
    assert "user" in data, "Response missing 'user' field"
    assert "accessToken" in data, "Response missing 'accessToken' field"
    assert "refreshToken" in data, "Response missing 'refreshToken' field"
    
    user = data["user"]
    assert "id" in user, "User missing 'id' field"
    assert "email" in user, "User missing 'email' field"
    assert "name" in user, "User missing 'name' field"
    assert user["email"] == login_payload["email"], "User email does not match request"
    
    # Validate tokens are present and non-empty
    assert data["accessToken"], "Access token is empty"
    assert data["refreshToken"], "Refresh token is empty"

test_auth_login_returns_tokens_successfully()
