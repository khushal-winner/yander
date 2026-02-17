import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_auth_register_creates_user_successfully():
    url = f"{BASE_URL}/auth/register"
    payload = {
        "email": "authuser+tc008@example.com",
        "password": "password123",
        "name": "Auth User TC008"
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
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
    assert user["email"] == payload["email"], "User email does not match request"
    assert user["name"] == payload["name"], "User name does not match request"
    
    # Validate tokens are present and non-empty
    assert data["accessToken"], "Access token is empty"
    assert data["refreshToken"], "Refresh token is empty"

test_auth_register_creates_user_successfully()
