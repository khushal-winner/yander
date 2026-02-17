import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://localhost:8000"
AUTH_USERNAME = "test@test.com"
TIMEOUT = 30

def test_post_users_missing_email_returns_error():
    url = f"{BASE_URL}/users"
    headers = {"Content-Type": "application/json"}
    payload = {"name": "Bob"}  # Missing email field
    auth = HTTPBasicAuth(AUTH_USERNAME, '')

    try:
        response = requests.post(url, json=payload, headers=headers, auth=auth, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"
    try:
        resp_json = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    assert "error" in resp_json, "Response JSON does not contain 'error' key"
    assert isinstance(resp_json["error"], str) and len(resp_json["error"]) > 0, "'error' value should be a non-empty string"

test_post_users_missing_email_returns_error()