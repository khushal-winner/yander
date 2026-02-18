import requests
import uuid
import random
import string

base_url = "http://localhost:8000"
timeout = 30

auth_username = "test@test.com"

def get_access_token():
    # Login to get accessToken and refreshToken
    login_url = f"{base_url}/auth/login"
    login_payload = {
        "email": auth_username,
        "password": "password123"  # Assuming a default password for the test user
    }
    try:
        r = requests.post(login_url, json=login_payload, timeout=timeout)
        r.raise_for_status()
        tokens = r.json()
        return tokens.get("accessToken")
    except Exception as e:
        raise RuntimeError(f"Failed to login and get access token: {e}")

def create_workspace(access_token):
    url = f"{base_url}/api/workspaces"
    slug = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    payload = {
        "name": "Test Workspace " + str(uuid.uuid4()),
        "slug": slug
    }
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    r = requests.post(url, json=payload, headers=headers, timeout=timeout)
    r.raise_for_status()
    return r.json()

def delete_workspace(access_token, workspace_id):
    url = f"{base_url}/api/workspaces/{workspace_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    r = requests.delete(url, headers=headers, timeout=timeout)
    if r.status_code not in (204, 404):
        r.raise_for_status()

def test_post_api_invitations_send_invitation_to_join_workspace():
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    workspace = None
    invitation_id = None
    try:
        # Create a workspace to invite someone to
        workspace = create_workspace(access_token)
        workspace_id = workspace.get("id")
        assert workspace_id, "Workspace creation did not return an id"

        # Prepare invitation payload
        invitation_email = f"invitee_{uuid.uuid4().hex[:8]}@example.com"
        invitation_role = "member"
        invitation_url = f"{base_url}/api/invitations"
        invitation_payload = {
            "email": invitation_email,
            "workspaceId": workspace_id,
            "role": invitation_role
        }

        # Send POST /api/invitations
        r = requests.post(invitation_url, json=invitation_payload, headers=headers, timeout=timeout)
        assert r.status_code == 201, f"Expected status code 201, got {r.status_code}"
        invitation = r.json()
        assert invitation.get("id"), "Invitation response missing 'id'"
        assert invitation.get("email") == invitation_email, "Invitation email mismatch"
        assert invitation.get("workspaceId") == workspace_id, "Invitation workspaceId mismatch"
        assert invitation.get("role") == invitation_role, "Invitation role mismatch"

        invitation_id = invitation.get("id")

    finally:
        # Cleanup: delete invitation if exists
        if invitation_id:
            try:
                del_url = f"{base_url}/api/invitations/{invitation_id}"
                del_resp = requests.delete(del_url, headers=headers, timeout=timeout)
                if del_resp.status_code not in (204, 404):
                    del_resp.raise_for_status()
            except Exception:
                pass

        # Cleanup: delete workspace if exists
        if workspace and workspace.get("id"):
            try:
                delete_workspace(access_token, workspace["id"])
            except Exception:
                pass

test_post_api_invitations_send_invitation_to_join_workspace()