import requests

BASE_URL = "http://localhost:8000"
REGISTER_URL = f"{BASE_URL}/auth/register"
LOGIN_URL = f"{BASE_URL}/auth/login"
AUTH_ME_URL = f"{BASE_URL}/auth/me"
TIMEOUT = 30

def test_get_auth_me_fetch_current_user_information():
    email = "test@test.com"
    password = "TestPass123!"
    name = "Test User"

    # Register user
    register_payload = {
        "email": email,
        "password": password,
        "name": name
    }
    registered = False
    try:
        r = requests.post(REGISTER_URL, json=register_payload, timeout=TIMEOUT)
        if r.status_code == 201:
            registered = True
        elif r.status_code == 400:
            # Possibly user exists, try login
            pass
        else:
            r.raise_for_status()
    except requests.RequestException as e:
        # If failed for any reason other than user exists, fail the test
        raise AssertionError(f"Registration request failed: {e}")

    # Login to get access token
    login_payload = {
        "email": email,
        "password": password,
    }
    try:
        r = requests.post(LOGIN_URL, json=login_payload, timeout=TIMEOUT)
        assert r.status_code == 200, f"Login failed, expected 200 got {r.status_code}, body: {r.text}"
        tokens = r.json()
        assert "accessToken" in tokens, "accessToken missing in response"
        access_token = tokens["accessToken"]
    except requests.RequestException as e:
        raise AssertionError(f"Login request failed: {e}")

    # Call GET /auth/me with valid access token
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    try:
        r = requests.get(AUTH_ME_URL, headers=headers, timeout=TIMEOUT)
        assert r.status_code == 200, f"GET /auth/me failed, expected 200 got {r.status_code}"
        user = r.json()
        assert isinstance(user, dict), "Response is not a JSON object"
        assert "email" in user and user["email"].lower() == email.lower(), "Returned user email does not match"
    except requests.RequestException as e:
        raise AssertionError(f"GET /auth/me request failed: {e}")
    finally:
        # Clean up: delete the created user if registered in this test run
        if registered:
            # User deletion endpoint is /users/:id and no auth required per PRD
            user_id = user.get("id")
            if user_id:
                try:
                    del_resp = requests.delete(f"{BASE_URL}/users/{user_id}", timeout=TIMEOUT)
                    # 204 expected or user may not exist if deleted prior
                except Exception:
                    pass

test_get_auth_me_fetch_current_user_information()