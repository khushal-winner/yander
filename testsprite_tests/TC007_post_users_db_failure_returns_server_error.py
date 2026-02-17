import requests
from requests.auth import HTTPBasicAuth

def test_post_users_db_failure_returns_server_error():
    base_url = "http://localhost:8000"
    url = f"{base_url}/users"

    auth = HTTPBasicAuth('test@test.com', '')
    headers = {
        "Content-Type": "application/json",
    }

    # Payload for user creation
    payload = {
        "email": "simulate-db-failure@example.com",
        "name": "DB Failure Test"
    }

    # To simulate a DB failure, we expect the test environment or server
    # to be configured accordingly (e.g. by mocking prisma or the DB connection).
    # Since we only have API-level access here, we send the request and assert
    # a 500 error with a JSON error message is returned.

    try:
        response = requests.post(url, json=payload, headers=headers, auth=auth, timeout=30)
    except requests.RequestException as e:
        assert False, f"Request failed with exception: {e}"

    assert response.status_code == 500, f"Expected status code 500, got {response.status_code}"

    try:
        json_response = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    assert "error" in json_response and isinstance(json_response["error"], str) and len(json_response["error"]) > 0, \
        "Response JSON must contain a non-empty 'error' string field"

test_post_users_db_failure_returns_server_error()