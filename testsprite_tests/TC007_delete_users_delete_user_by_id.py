import requests

BASE_URL = "http://localhost:8000"

def test_delete_user_by_id():
    timeout = 30

    # Step 1: Create a new user to ensure a user exists for deletion
    create_user_payload = {
        "email": "tempuser_delete_test@example.com",
        "name": "Temp User Delete Test"
    }
    try:
        create_resp = requests.post(f"{BASE_URL}/users", json=create_user_payload, timeout=timeout)
        assert create_resp.status_code == 201, f"User creation failed with status {create_resp.status_code}"
        user = create_resp.json()
        user_id = user.get("id")
        assert user_id is not None, "Created user response does not contain 'id'"

        # Step 2: Delete the user by ID
        delete_resp = requests.delete(f"{BASE_URL}/users/{user_id}", timeout=timeout)
        assert delete_resp.status_code == 204, f"User deletion failed with status {delete_resp.status_code}"
        assert not delete_resp.content, "Response content for DELETE /users/:id should be empty"

        # Step 3: Verify deletion by attempting to delete again (should return 404)
        delete_again_resp = requests.delete(f"{BASE_URL}/users/{user_id}", timeout=timeout)
        assert delete_again_resp.status_code == 404, f"Expected 404 when deleting non-existent user, got {delete_again_resp.status_code}"

    finally:
        # Cleanup: Attempt to delete user if still exists
        if 'user_id' in locals():
            requests.delete(f"{BASE_URL}/users/{user_id}", timeout=timeout)

test_delete_user_by_id()