import requests

def test_tc010_get_root_health_check_endpoint():
    base_url = "http://localhost:8000"
    url = f"{base_url}/"
    try:
        response = requests.get(url, timeout=30)
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        # The body should contain a "Hello World" message indicating server is running
        # Accept either plain text or JSON with such message
        try:
            data = response.json()
            assert any("hello" in str(v).lower() and "world" in str(v).lower() for v in data.values()), \
                "Response JSON does not contain 'Hello World' message"
        except ValueError:
            # Not JSON, check text body
            body_text = response.text.lower()
            assert "hello" in body_text and "world" in body_text, "Response text does not contain 'Hello World'"
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

test_tc010_get_root_health_check_endpoint()