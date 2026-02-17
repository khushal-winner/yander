import requests

def test_get_error_endpoint_returns_server_error():
    base_url = "http://localhost:8000"
    url = f"{base_url}/error"
    headers = {
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 500, f"Expected status code 500 but got {response.status_code}"
    try:
        json_response = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    expected_response = {"error": "Something broke!"}
    assert json_response == expected_response, f"Expected response {expected_response} but got {json_response}"

test_get_error_endpoint_returns_server_error()
