import requests

def test_post_auth_login_valid_credentials():
    base_url = "http://localhost:8000"
    login_url = f"{base_url}/auth/login"
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": "test@test.com",
        "password": "testpassword"  # password must be correct for this test to pass
    }
    # We don't have the password explicitly in the PRD or instructions
    # Assuming it must be "testpassword" or must be replaced by a valid password if known.
    try:
        response = requests.post(login_url, json=payload, headers=headers, timeout=30)
        assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
        data = response.json()
        assert "accessToken" in data and isinstance(data["accessToken"], str) and data["accessToken"], "Missing or invalid accessToken"
        assert "refreshToken" in data and isinstance(data["refreshToken"], str) and data["refreshToken"], "Missing or invalid refreshToken"
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

test_post_auth_login_valid_credentials()