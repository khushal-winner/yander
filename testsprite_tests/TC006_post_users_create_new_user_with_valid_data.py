import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_post_users_create_new_user_with_valid_data():
    url = f"{BASE_URL}/users"
    headers = {
        "Content-Type": "application/json"
    }
    # Unique email to avoid duplication issues
    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
    payload = {
        "email": unique_email,
        "name": "Test User"
    }

    created_user_id = None
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
        # Assert status code 201 Created
        assert response.status_code == 201, f"Expected status 201, got {response.status_code}"
        response_json = response.json()
        # Assert returned user object has email and name matching request
        assert response_json.get("email") == unique_email, "Response email mismatch"
        assert response_json.get("name") == "Test User", "Response name mismatch"
        # Assert user id exists and is not empty
        assert "id" in response_json and response_json["id"], "User id missing in response"
        created_user_id = response_json["id"]
    finally:
        # Cleanup: delete created user if created
        if created_user_id:
            delete_url = f"{BASE_URL}/users/{created_user_id}"
            try:
                del_response = requests.delete(delete_url, timeout=TIMEOUT)
                # Optionally assert 204 deletion success, but ignore errors silently here
                if del_response.status_code != 204:
                    print(f"Warning: Failed to delete user {created_user_id}, status code {del_response.status_code}")
            except Exception as e:
                print(f"Exception during cleanup delete: {e}")

test_post_users_create_new_user_with_valid_data()
