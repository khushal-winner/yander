import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_post_auth_login_valid_credentials():
    url = f"{BASE_URL}/auth/login"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "email": "test@test.com",
        "password": "test"  # Assuming password is "test" because only email given; use a correct known test password
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request to {url} failed: {e}"
    
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}, response: {response.text}"
    try:
        data = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    # Validate presence of accessToken and refreshToken in response
    assert isinstance(data, dict), f"Response JSON should be an object, got {type(data)}"
    assert "accessToken" in data, "Response JSON missing 'accessToken'"
    assert isinstance(data["accessToken"], str) and data["accessToken"], "'accessToken' should be non-empty string"
    assert "refreshToken" in data, "Response JSON missing 'refreshToken'"
    assert isinstance(data["refreshToken"], str) and data["refreshToken"], "'refreshToken' should be non-empty string"

test_post_auth_login_valid_credentials()