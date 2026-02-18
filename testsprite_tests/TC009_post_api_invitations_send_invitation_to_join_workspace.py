import requests
import uuid

BASE_URL = "http://localhost:8000"
AUTH_USERNAME = "test@test.com"
AUTH_TOKEN_HEADER = "Authorization"
TIMEOUT = 30

def get_access_token():
    login_url = BASE_URL + "/auth/login"
    login_data = {
        "email": AUTH_USERNAME,
        "password": "password"  # Assuming password; if unknown, register/login step needed
    }
    try:
        resp = requests.post(login_url, json=login_data, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()["accessToken"]
    except Exception:
        # If login fails because password unknown, register user with fixed password then login
        register_url = BASE_URL + "/auth/register"
        register_data = {
            "email": AUTH_USERNAME,
            "password": "password",
            "name": "Test User"
        }
        r_reg = requests.post(register_url, json=register_data, timeout=TIMEOUT)
        r_reg.raise_for_status()
        r_login = requests.post(login_url, json=login_data, timeout=TIMEOUT)
        r_login.raise_for_status()
        return r_login.json()["accessToken"]

def create_workspace(token):
    url = BASE_URL + "/api/workspaces"
    workspace_name = "TestWorkspace_" + str(uuid.uuid4())
    workspace_slug = "testworkspace-" + str(uuid.uuid4())[:8]
    headers = {AUTH_TOKEN_HEADER: f"Bearer {token}"}
    body = {"name": workspace_name, "slug": workspace_slug}
    resp = requests.post(url, json=body, headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()

def delete_workspace(token, workspace_id):
    url = f"{BASE_URL}/api/workspaces/{workspace_id}"
    headers = {AUTH_TOKEN_HEADER: f"Bearer {token}"}
    resp = requests.delete(url, headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()
    # No content response expected 204

def test_post_api_invitations_send_invitation():
    access_token = get_access_token()
    headers = {AUTH_TOKEN_HEADER: f"Bearer {access_token}"}

    # Create workspace to use for invitation
    workspace = create_workspace(access_token)
    workspace_id = workspace["id"]

    invitation_email = f"invitee_{uuid.uuid4().hex[:8]}@example.com"
    invitation_role = "member"

    invitations_url = BASE_URL + "/api/invitations"
    invitation_data = {
        "email": invitation_email,
        "workspaceId": workspace_id,
        "role": invitation_role
    }

    try:
        response = requests.post(invitations_url, json=invitation_data, headers=headers, timeout=TIMEOUT)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        invitation = response.json()
        assert isinstance(invitation, dict), "Invitation response is not an object"
        assert invitation.get("email") == invitation_email, "Invitation email does not match"
        assert invitation.get("workspaceId") == workspace_id, "Invitation workspaceId does not match"
        assert invitation.get("role") == invitation_role, "Invitation role does not match"
        assert "id" in invitation and invitation["id"], "Invitation id missing or empty"
    finally:
        # Cleanup: delete the created workspace which implicitly cleans up related invitations
        delete_workspace(access_token, workspace_id)

test_post_api_invitations_send_invitation()