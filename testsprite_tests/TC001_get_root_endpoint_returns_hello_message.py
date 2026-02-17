import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://localhost:8000"
AUTH_USERNAME = "test@test.com"
TIMEOUT = 30

def test_get_root_endpoint_returns_hello_message():
    try:
        response = requests.get(
            f"{BASE_URL}/",
            auth=HTTPBasicAuth(AUTH_USERNAME, ''),
            timeout=TIMEOUT
        )
        # Assert status code
        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        # Assert response json content
        json_data = response.json()
        assert json_data == {"message": "Hello World"}, f"Expected JSON {{'message': 'Hello World'}} but got {json_data}"
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

test_get_root_endpoint_returns_hello_message()