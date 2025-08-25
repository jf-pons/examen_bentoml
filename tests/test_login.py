import pytest
import requests
from tests.constants import LOGIN_URL
from src.constants import JWT_TTL_SECONDS


class TestLogin:
    def test_login_correct_credentials(self, credentials):

        r = requests.post(url=LOGIN_URL, json={"credentials": credentials}, timeout=1)

        assert r.status_code == 200
        assert "access_token" in r.json()
        assert "token_type" in r.json() and r.json()["token_type"] == "bearer"
        assert "expires_in" in r.json() and r.json()["expires_in"] == JWT_TTL_SECONDS

    @pytest.mark.parametrize(
        "username,password",
        [
            ["user123", "password456"],
            ["user456", "password123"],
            ["unknown", "password"],
        ],
    )
    def test_login_wrong_credentials(self, username, password):
        credentials = {"username": username, "password": password}

        r = requests.post(url=LOGIN_URL, json={"credentials": credentials}, timeout=1)

        assert r.status_code == 401
