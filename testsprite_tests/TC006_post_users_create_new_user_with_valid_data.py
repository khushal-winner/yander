import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_post_users_create_new_user_with_valid_data():
    url = f"{BASE_URL}/users"
    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
    payload = {
        "email": unique_email,
        "name": "Test User"
    }
    headers = {
        "Content-Type": "application/json"
    }
    created_user_id = None
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
        assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"
        data = response.json()
        assert "id" in data, "Response JSON does not contain 'id'"
        assert data["email"] == unique_email, f"Expected email {unique_email} but got {data['email']}"
        assert data["name"] == "Test User", f"Expected name 'Test User' but got {data['name']}"
        created_user_id = data["id"]
    finally:
        if created_user_id:
            delete_url = f"{BASE_URL}/users/{created_user_id}"
            try:
                del_resp = requests.delete(delete_url, timeout=TIMEOUT)
                assert del_resp.status_code == 204, f"Cleanup delete user failed with status code {del_resp.status_code}"
            except Exception:
                pass

test_post_users_create_new_user_with_valid_data()