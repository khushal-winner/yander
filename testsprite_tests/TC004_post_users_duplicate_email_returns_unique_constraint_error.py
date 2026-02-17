import requests

base_url = "http://localhost:8000"
timeout = 30

def test_post_users_duplicate_email_returns_unique_constraint_error():
    created_user_id = None
    user_email = "duplicateuser@example.com"
    headers = {"Content-Type": "application/json"}

    # Step 1: Create a new user with the email to ensure duplication
    create_payload = {
        "email": user_email,
        "name": "Original User"
    }
    try:
        create_response = requests.post(
            f"{base_url}/users",
            json=create_payload,
            headers=headers,
            timeout=timeout
        )
        assert create_response.status_code == 200, f"Initial user creation failed with status {create_response.status_code}"
        created_user = create_response.json()
        created_user_id = created_user.get("id")
        assert created_user_id, "Created user ID not found in response"

        # Step 2: Attempt to create another user with the same email
        duplicate_payload = {
            "email": user_email,
            "name": "Duplicate User"
        }
        duplicate_response = requests.post(
            f"{base_url}/users",
            json=duplicate_payload,
            headers=headers,
            timeout=timeout
        )
        # Validate status code and error message
        assert duplicate_response.status_code == 400, f"Expected 400 status for duplicate email, got {duplicate_response.status_code}"
        error_body = duplicate_response.json()
        assert "error" in error_body, "Error message key missing in response"
        assert "Unique constraint failed on the fields: (email)" in error_body["error"], \
            f"Unexpected error message: {error_body['error']}"

    finally:
        # Cleanup: Delete the created user if exists
        if created_user_id:
            try:
                requests.delete(
                    f"{base_url}/users/{created_user_id}",
                    timeout=timeout
                )
            except Exception:
                pass  # Ignore cleanup errors silently

test_post_users_duplicate_email_returns_unique_constraint_error()
