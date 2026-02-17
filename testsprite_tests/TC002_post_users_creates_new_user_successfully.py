import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_post_users_creates_new_user_successfully():
    url = f"{BASE_URL}/users"
    payload = {
        "email": "testuser+tc002@example.com",
        "name": "Test User TC002"
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    # Validate presence and types of fields
    for field in ['id', 'email', 'name', 'createdAt', 'updatedAt']:
        assert field in data, f"Response JSON missing '{field}' field"
        assert isinstance(data[field], str), f"Field '{field}' should be a string"
    assert data['email'] == payload['email'], "Response email does not match request"
    assert data['name'] == payload['name'], "Response name does not match request"

    # Cleanup: delete created user by ID
    user_id = data['id']
    delete_url = f"{BASE_URL}/users/{user_id}"
    try:
        del_response = requests.delete(delete_url, timeout=TIMEOUT)
        # Allow 200 or 204 as successful delete responses
        assert del_response.status_code in (200, 204), f"Failed to delete user in cleanup, status: {del_response.status_code}"
    except requests.RequestException as e:
        assert False, f"Cleanup delete request failed: {e}"

test_post_users_creates_new_user_successfully()
