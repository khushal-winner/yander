import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_delete_user_by_id():
    # Create user to delete
    user_data = {
        "email": f"delete_test_user_{str(uuid.uuid4())[:8]}@example.com",
        "name": "Delete Test User"
    }

    create_resp = requests.post(
        f"{BASE_URL}/users",
        json=user_data,
        timeout=TIMEOUT
    )
    assert create_resp.status_code == 201, f"User creation failed: {create_resp.text}"
    user = create_resp.json()
    user_id = user.get("id")
    assert user_id, "Created user ID missing in response"

    try:
        # Now delete the user by ID
        delete_resp = requests.delete(
            f"{BASE_URL}/users/{user_id}",
            timeout=TIMEOUT
        )
        assert delete_resp.status_code == 204, f"Expected 204 No Content but got {delete_resp.status_code}, response: {delete_resp.text}"

        # Verify user no longer exists by attempting to delete again, expect 404
        delete_again_resp = requests.delete(
            f"{BASE_URL}/users/{user_id}",
            timeout=TIMEOUT
        )
        assert delete_again_resp.status_code == 404, f"Expected 404 User not found on second delete but got {delete_again_resp.status_code}"
    finally:
        # Clean up in case deletion failed
        requests.delete(f"{BASE_URL}/users/{user_id}", timeout=TIMEOUT)

test_delete_user_by_id()