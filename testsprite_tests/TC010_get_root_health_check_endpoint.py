import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_get_root_health_check_endpoint():
    url = f"{BASE_URL}/"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        # Check status code is 200
        assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
        # Check response content includes expected Hello World message
        # The PRD says "Receive 200 with Hello World message"
        # We'll accept json or plain text containing 'Hello World'
        content_type = response.headers.get('Content-Type','')
        if 'application/json' in content_type:
            body = response.json()
            # The exact key is not specified, so check values
            assert any("hello" in str(v).lower() and "world" in str(v).lower() for v in body.values()), "Response JSON does not contain expected Hello World message"
        else:
            body = response.text
            assert "hello" in body.lower() and "world" in body.lower(), "Response text does not contain expected Hello World message"
    except requests.RequestException as e:
        assert False, f"Request to {url} failed with exception: {e}"

test_get_root_health_check_endpoint()