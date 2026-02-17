import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_auth_register_duplicate_email_returns_error():
    url = f"{BASE_URL}/auth/register"
    payload = {
        "email": "duplicate+tc011@example.com",
        "password": "password123",
        "name": "Duplicate User TC011"
    }
    headers = {
        "Content-Type": "application/json"
    }

    # First registration should succeed
    try:
        first_response = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
        assert first_response.status_code == 201, f"First registration failed with status {first_response.status_code}"
    except requests.RequestException as e:
        assert False, f"First registration request failed: {e}"

    # Second registration with same email should fail
    try:
        second_response = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Second registration request failed: {e}"

    assert second_response.status_code == 400, f"Expected status code 400 for duplicate email, got {second_response.status_code}"
    try:
        data = second_response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    assert "error" in data, "Response missing 'error' field"
    assert data["error"] == "Email already registered", f"Expected 'Email already registered' error, got: {data['error']}"

test_auth_register_duplicate_email_returns_error()
