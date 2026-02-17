import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_auth_login_invalid_credentials_returns_error():
    url = f"{BASE_URL}/auth/login"
    
    # Test with wrong password
    wrong_password_payload = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=wrong_password_payload, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 401, f"Expected status code 401 for wrong credentials, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    assert "error" in data, "Response missing 'error' field"
    assert data["error"] == "Invalid credentials", f"Expected 'Invalid credentials' error, got: {data['error']}"

    # Test with missing fields
    missing_fields_payload = {
        "email": "test@example.com"
        # Missing password
    }

    try:
        response = requests.post(url, json=missing_fields_payload, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 400, f"Expected status code 400 for missing fields, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    assert "error" in data, "Response missing 'error' field"
    assert data["error"] == "Missing fields", f"Expected 'Missing fields' error, got: {data['error']}"

test_auth_login_invalid_credentials_returns_error()
