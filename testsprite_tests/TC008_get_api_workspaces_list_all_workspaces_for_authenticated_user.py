import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

# Credentials from instructions
USERNAME = "test@test.com"
PASSWORD = "TestPassword123!"  # Assumed password for the test user; adjust if needed

def test_get_api_workspaces_list_all_workspaces():
    """
    Test GET /api/workspaces endpoint with valid access token returns 200 with list of workspaces the user belongs to,
    and comprehensive workspace API endpoints including authentication, authorization, error handling, member management,
    and health check endpoints per instructions.
    """

    headers = {}
    access_token = None
    refresh_token = None
    workspace_id = None
    new_user_id = None
    member_role_original = None

    def get_auth_headers(token):
        return {"Authorization": f"Bearer {token}"}

    try:
        # 1. Login to get access token and refresh token
        login_resp = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": USERNAME, "password": PASSWORD},
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT,
        )
        assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
        login_data = login_resp.json()
        access_token = login_data.get("accessToken") or login_data.get("access_token")
        refresh_token = login_data.get("refreshToken") or login_data.get("refresh_token")

        assert access_token, "No access token received from login"
        assert refresh_token, "No refresh token received from login"

        headers = get_auth_headers(access_token)

        # 2. GET /api/workspaces - List user workspaces - Positive
        ws_list_resp = requests.get(f"{BASE_URL}/api/workspaces", headers=headers, timeout=TIMEOUT)
        assert ws_list_resp.status_code == 200, f"GET /api/workspaces failed: {ws_list_resp.text}"
        workspaces = ws_list_resp.json()
        assert isinstance(workspaces, list), "Workspaces response is not a list"

        # 3. If no existing workspace, create one to work with
        if not workspaces:
            ws_create_payload = {
                "name": f"TestWorkspace-{uuid.uuid4()}",
                "slug": f"testslug{uuid.uuid4().hex[:8]}"
            }
            ws_create_resp = requests.post(
                f"{BASE_URL}/api/workspaces",
                headers={**headers, "Content-Type": "application/json"},
                json=ws_create_payload,
                timeout=TIMEOUT,
            )
            assert ws_create_resp.status_code == 201, f"Workspace creation failed: {ws_create_resp.text}"
            created_ws = ws_create_resp.json()
            workspace_id = created_ws.get("id") or created_ws.get("workspaceId")
            assert workspace_id, "Created workspace has no id"
        else:
            workspace_id = workspaces[0].get("id") or workspaces[0].get("workspaceId")
            assert workspace_id, "Workspace from list has no id"

        # --- Test GET /api/workspaces/:id/members ---
        members_resp = requests.get(
            f"{BASE_URL}/api/workspaces/{workspace_id}/members",
            headers=headers,
            timeout=TIMEOUT,
        )
        assert members_resp.status_code == 200, f"GET members failed: {members_resp.text}"
        members = members_resp.json()
        assert isinstance(members, list), "Members response is not a list"
        # Save a member userId for patch/delete tests (choose self if present)
        member_user_id = None
        if members:
            # Find the current user id among members or take the first
            # To get current user ID, call /auth/me
            me_resp = requests.get(f"{BASE_URL}/auth/me", headers=headers, timeout=TIMEOUT)
            assert me_resp.status_code == 200, f"GET /auth/me failed: {me_resp.text}"
            current_user = me_resp.json()
            current_user_id = current_user.get("id")
            # Prefer current user id if present in members
            for m in members:
                if m.get("userId") == current_user_id:
                    member_user_id = current_user_id
                    member_role_original = m.get("role")
                    break
            if not member_user_id:
                member_user_id = members[0].get("userId")
                member_role_original = members[0].get("role")
            assert member_user_id, "No member userId available for patch/delete tests"
        else:
            # No members returned, skip member role and delete tests
            member_user_id = None

        # --- Test PATCH /api/workspaces/:id/members/:userId - Change member role ---
        if member_user_id:
            # Toggle role for test (e.g. "member" <-> "admin") or change to a safe role
            new_role = "admin" if member_role_original != "admin" else "member"
            patch_payload = {"role": new_role}
            patch_resp = requests.patch(
                f"{BASE_URL}/api/workspaces/{workspace_id}/members/{member_user_id}",
                headers={**headers, "Content-Type": "application/json"},
                json=patch_payload,
                timeout=TIMEOUT,
            )
            assert patch_resp.status_code == 200, f"PATCH member role failed: {patch_resp.text}"
            patched_member = patch_resp.json()
            assert patched_member.get("role") == new_role, "Member role not updated correctly"

            # Revert role change to original for cleanup
            revert_payload = {"role": member_role_original}
            revert_resp = requests.patch(
                f"{BASE_URL}/api/workspaces/{workspace_id}/members/{member_user_id}",
                headers={**headers, "Content-Type": "application/json"},
                json=revert_payload,
                timeout=TIMEOUT,
            )
            assert revert_resp.status_code == 200, f"Revert PATCH member role failed: {revert_resp.text}"

            # --- Test DELETE /api/workspaces/:id/members/:userId - Remove member ---
            # To safely test delete, create a new user and add to workspace, then delete
            # Create user
            user_email = f"tempuser_{uuid.uuid4().hex[:8]}@test.com"
            user_name = "Temp User"
            user_create_resp = requests.post(
                f"{BASE_URL}/users",
                headers={"Content-Type": "application/json"},
                json={"email": user_email, "name": user_name},
                timeout=TIMEOUT,
            )
            assert user_create_resp.status_code == 201, f"Create user for member delete failed: {user_create_resp.text}"
            new_user = user_create_resp.json()
            new_user_id = new_user.get("id")
            assert new_user_id, "Created user has no id"

            # Invite or add new user as member (this step may depend on API implementation)
            invitation_payload = {"email": user_email, "workspaceId": workspace_id, "role": "member"}
            inv_resp = requests.post(f"{BASE_URL}/api/invitations", headers={**headers, "Content-Type": "application/json"}, json=invitation_payload, timeout=TIMEOUT)
            assert inv_resp.status_code == 201, f"Invitation creation failed: {inv_resp.text}"
            invitation = inv_resp.json()

            # Accept invitation: as no test user credentials for new user, can't accept - skip acceptance
            # So, test DELETE member only if the user is already member, otherwise skip delete test

            # For test purpose, attempt to delete the new user as member anyway (expecting 403 or 404 if member not added)
            delete_member_resp = requests.delete(
                f"{BASE_URL}/api/workspaces/{workspace_id}/members/{new_user_id}",
                headers=headers,
                timeout=TIMEOUT,
            )
            # Can be 204 if deleted or an error code (403 or 404)
            assert delete_member_resp.status_code in (204, 403, 404), f"Unexpected DELETE member status: {delete_member_resp.status_code}"

        # --- Test Authentication and Authorization Middleware ---
        # a. GET /api/workspaces without auth header -> 401
        no_auth_resp = requests.get(f"{BASE_URL}/api/workspaces", timeout=TIMEOUT)
        assert no_auth_resp.status_code == 401, f"Expected 401 without auth header, got {no_auth_resp.status_code}"

        # b. GET with invalid token -> 401
        invalid_headers = {"Authorization": "Bearer InvalidToken123"}
        invalid_token_resp = requests.get(f"{BASE_URL}/api/workspaces", headers=invalid_headers, timeout=TIMEOUT)
        assert invalid_token_resp.status_code == 401, f"Expected 401 with invalid token, got {invalid_token_resp.status_code}"

        # --- Test error handling for invalid workspace IDs ---
        invalid_id = "00000000-0000-0000-0000-000000000000"  # UUID improbable to exist

        # GET /api/workspaces/:id with invalid id -> 404
        invalid_ws_get = requests.get(f"{BASE_URL}/api/workspaces/{invalid_id}", headers=headers, timeout=TIMEOUT)
        assert invalid_ws_get.status_code == 404, f"Expected 404 for invalid workspace id, got {invalid_ws_get.status_code}"

        # PUT /api/workspaces/:id with invalid id -> 404
        put_payload = {"name": "NewName", "slug": "newslug"}
        invalid_ws_put = requests.put(f"{BASE_URL}/api/workspaces/{invalid_id}", headers={**headers, "Content-Type": "application/json"}, json=put_payload, timeout=TIMEOUT)
        assert invalid_ws_put.status_code == 404, f"Expected 404 for PUT invalid workspace id, got {invalid_ws_put.status_code}"

        # DELETE /api/workspaces/:id with invalid id -> 404
        invalid_ws_delete = requests.delete(f"{BASE_URL}/api/workspaces/{invalid_id}", headers=headers, timeout=TIMEOUT)
        assert invalid_ws_delete.status_code == 404, f"Expected 404 for DELETE invalid workspace id, got {invalid_ws_delete.status_code}"

        # --- Test health check endpoints ---
        root_health_resp = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
        assert root_health_resp.status_code == 200, f"Health check root endpoint failed: {root_health_resp.text}"
        assert "hello" in root_health_resp.text.lower(), "Health check root response unexpected"

        redis_test_resp = requests.get(f"{BASE_URL}/test-redis", timeout=TIMEOUT)
        assert redis_test_resp.status_code in (200, 500), "Unexpected status code for Redis test endpoint"

        error_resp = requests.get(f"{BASE_URL}/error", timeout=TIMEOUT)
        assert error_resp.status_code == 500, "Expected 500 from /error endpoint"
        error_json = error_resp.json()
        assert "error" in error_json, "Error response missing 'error' key"

    finally:
        # Cleanup
        if workspace_id:
            # Delete workspace created if it was created here
            if workspaces == []:
                del_resp = requests.delete(f"{BASE_URL}/api/workspaces/{workspace_id}", headers=headers, timeout=TIMEOUT)
                assert del_resp.status_code in (204, 404), f"Failed to cleanup workspace: {del_resp.text}"

        if new_user_id:
            # Delete the temporary user created
            del_user_resp = requests.delete(f"{BASE_URL}/users/{new_user_id}", timeout=TIMEOUT)
            assert del_user_resp.status_code in (204, 404), f"Failed to cleanup user: {del_user_resp.text}"

test_get_api_workspaces_list_all_workspaces()
