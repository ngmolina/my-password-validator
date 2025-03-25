# test_main.py
import pytest
from main import app


@pytest.fixture
def client():
    """
    Pytest fixture that creates a Flask test client from the 'app' in main.py.
    """
    with app.test_client() as client:
        yield client


def test_root_endpoint(client):
    """
    Test the GET '/' endpoint to ensure it returns
    the greeting and a 200 status code.
    """
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Hello from my Password Validator!" in resp.data


def test_valid_password(client):
    """
    Test a valid password that meets all requirements:
    - Length >= 8
    - At least 2 uppercase letters
    - At least 2 digits
    - At least 1 special character from !@#$%^&*
    """
    resp = client.post("/v1/checkPassword", json={"password": "ABcd12!34"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("valid") is True
    assert data.get("reason") == ""


def test_password_too_short(client):
    """
    Test a password that is too short (less than 8 characters).
    """
    resp = client.post("/v1/checkPassword", json={"password": "Ab3!"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("valid") is False
    assert "at least 8 characters" in data.get("reason").lower()


def test_password_missing_uppercase(client):
    """
    Test a password that doesn't have enough uppercase letters.
    """
    resp = client.post("/v1/checkPassword", json={"password": "Abcdef12!"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("valid") is False
    assert "uppercase" in data.get("reason").lower()


def test_password_missing_digits(client):
    """
    Test a password that doesn't have enough digits.
    """
    resp = client.post("/v1/checkPassword", json={"password": "ABcdefg1!"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("valid") is False
    assert "digits" in data.get("reason").lower()


def test_password_missing_special_char(client):
    """
    Test a password that doesn't have any special characters.
    """
    resp = client.post("/v1/checkPassword", json={"password": "ABcdef12"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("valid") is False
    assert "special character" in data.get("reason").lower()


def test_password_empty(client):
    """
    Test with an empty password.
    """
    resp = client.post("/v1/checkPassword", json={"password": ""})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("valid") is False


def test_complex_valid_password(client):
    """
    Test with a more complex valid password.
    """
    resp = client.post("/v1/checkPassword", json={"password": "P@ssW0rd123!"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("valid") is True
    assert data.get("reason") == ""


def test_missing_password_field(client):
    """
    Test the behavior when the password field is missing in the request.
    """
    resp = client.post("/v1/checkPassword", json={})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("valid") is False


def test_edge_case_exactly_minimum(client):
    """
    Test a password that meets exactly the minimum requirements.
    """
    resp = client.post("/v1/checkPassword", json={"password": "AB12345!"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("valid") is True
    assert data.get("reason") == ""


def test_wrong_request_method(client):
    """
    Test that using a GET request on the password endpoint returns an error.
    """
    resp = client.get("/v1/checkPassword")
    assert resp.status_code == 405  # Method Not Allowed