import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

USER_EMAIL = "test@test.com"
USER_PASSWORD = "TestPassword123!"

def test_get_api_workspaces_list_all_workspaces_for_authenticated_user():
    # Helper function to register a new user - used only if login fails for the test user
    def register_user(email, password):
        register_payload = {
            "email": email,
            "password": password,
            "name": "Test User"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=register_payload, timeout=TIMEOUT)
        assert response.status_code == 201
        return response.json()

    # Helper function to login and return accessToken and refreshToken
    def login_user(email, password):
        login_payload = {
            "email": email,
            "password": password
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_payload, timeout=TIMEOUT)
        return response

    # Attempt to login first
    login_resp = login_user(USER_EMAIL, USER_PASSWORD)
    if login_resp.status_code == 401:
        # User likely doesn't exist, register then login again
        register_user(USER_EMAIL, USER_PASSWORD)
        login_resp = login_user(USER_EMAIL, USER_PASSWORD)

    assert login_resp.status_code == 200, f"Login failed with status {login_resp.status_code}, body: {login_resp.text}"
    tokens = login_resp.json()
    access_token = tokens.get("accessToken")
    refresh_token = tokens.get("refreshToken")
    assert access_token, "No accessToken in login response"
    assert refresh_token, "No refreshToken in login response"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Create a new workspace to ensure user has at least one workspace
    workspace_name = f"test-workspace-{uuid.uuid4()}"
    workspace_slug = f"test-workspace-{uuid.uuid4()}"
    create_workspace_payload = {
        "name": workspace_name,
        "slug": workspace_slug
    }

    ws_create_resp = requests.post(f"{BASE_URL}/api/workspaces", headers=headers, json=create_workspace_payload, timeout=TIMEOUT)
    assert ws_create_resp.status_code == 201, f"Workspace creation failed: {ws_create_resp.text}"
    workspace = ws_create_resp.json()
    workspace_id = workspace.get("id")
    assert workspace_id, "Created workspace has no id"

    try:
        # Test GET /api/workspaces endpoint
        ws_list_resp = requests.get(f"{BASE_URL}/api/workspaces", headers=headers, timeout=TIMEOUT)
        assert ws_list_resp.status_code == 200, f"GET /api/workspaces failed: {ws_list_resp.text}"
        ws_list = ws_list_resp.json()
        assert isinstance(ws_list, list), "Response is not a list"
        # The created workspace should be in the list
        assert any(w.get("id") == workspace_id for w in ws_list), "Created workspace not found in workspace list"

        # Removed members endpoints tests - not part of PRD

        # 4. Test authentication and authorization middleware:
        # GET /api/workspaces without Authorization header -> expect 401
        ws_no_auth_resp = requests.get(f"{BASE_URL}/api/workspaces", timeout=TIMEOUT)
        assert ws_no_auth_resp.status_code == 401, f"GET /api/workspaces without auth should 401, got {ws_no_auth_resp.status_code}"

        # 5. Test error handling for invalid workspace ID for GET
        invalid_id = "invalid-id-1234"
        ws_invalid_resp = requests.get(f"{BASE_URL}/api/workspaces/{invalid_id}", headers=headers, timeout=TIMEOUT)
        assert ws_invalid_resp.status_code == 404, f"GET /api/workspaces/{invalid_id} should return 404, got {ws_invalid_resp.status_code}"

        # 6. Test error handling for invalid workspace ID for PUT
        put_payload = {"name": "newname", "slug": "newslug"}
        ws_put_invalid_resp = requests.put(f"{BASE_URL}/api/workspaces/{invalid_id}", headers=headers, json=put_payload, timeout=TIMEOUT)
        assert ws_put_invalid_resp.status_code == 404, f"PUT /api/workspaces/{invalid_id} should return 404, got {ws_put_invalid_resp.status_code}"

        # 7. Test error handling for invalid workspace ID for DELETE
        ws_del_invalid_resp = requests.delete(f"{BASE_URL}/api/workspaces/{invalid_id}", headers=headers, timeout=TIMEOUT)
        assert ws_del_invalid_resp.status_code == 404, f"DELETE /api/workspaces/{invalid_id} should return 404, got {ws_del_invalid_resp.status_code}"

        # 8. Test health check endpoint GET /
        health_resp = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
        assert health_resp.status_code == 200, f"Health check GET / failed with {health_resp.status_code}"
        health_text = health_resp.text.lower()
        assert "hello" in health_text or "world" in health_text, "Health check response unexpected"

        # 9. Test Redis connectivity endpoint GET /test-redis
        redis_resp = requests.get(f"{BASE_URL}/test-redis", timeout=TIMEOUT)
        # Accept 200 or 500 as per description
        assert redis_resp.status_code in (200, 500), f"GET /test-redis unexpected status {redis_resp.status_code}"

        # 10. Test error handling endpoint GET /error
        error_resp = requests.get(f"{BASE_URL}/error", timeout=TIMEOUT)
        assert error_resp.status_code == 500, f"GET /error expected status 500, got {error_resp.status_code}"
        error_body = error_resp.json()
        assert "error" in error_body, "GET /error response missing 'error' field"
    finally:
        # Clean up: delete the workspace created
        delete_resp = requests.delete(f"{BASE_URL}/api/workspaces/{workspace_id}", headers=headers, timeout=TIMEOUT)
        # Deletion may return 204 or possibly 404 if already deleted; accept both
        assert delete_resp.status_code in (204, 404), f"Workspace deletion unexpected status {delete_resp.status_code}"

test_get_api_workspaces_list_all_workspaces_for_authenticated_user()
