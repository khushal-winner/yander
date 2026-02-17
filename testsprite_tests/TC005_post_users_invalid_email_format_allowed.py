import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://localhost:8000"
AUTH_USERNAME = "test@test.com"

def test_post_users_invalid_email_format_not_allowed():
    url = f"{BASE_URL}/users"
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": "invalid-email-format",
        "name": "Eve"
    }
    auth = HTTPBasicAuth(AUTH_USERNAME, "")

    response = requests.post(url, json=payload, headers=headers, auth=auth, timeout=30)
    assert response.status_code == 400, f"Expected status code 400 but got {response.status_code}"

    error_resp = response.json()
    assert isinstance(error_resp, dict), "Response JSON is not a dictionary"
    assert "error" in error_resp and isinstance(error_resp["error"], str) and error_resp["error"], "Error message missing or invalid"


test_post_users_invalid_email_format_not_allowed()
