import time
import requests
import jwt
from src.constants import JWT_SECRET, JWT_ALGO
from tests.constants import PREDICT_URL


class TestAuthentication:
    def test_succesful_authentication(self, token, input_data):
        response = requests.post(
            PREDICT_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            json=input_data,
            timeout=20,
        )

        assert response.status_code == 200

    def test_failed_authentication_token_expired(self, credentials, input_data):
        payload = {
            "sub": credentials["username"],
            "exp": int(time.time()),
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

        time.sleep(0.1)  # Wait for the token to be expired

        response = requests.post(
            PREDICT_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            json=input_data,
            timeout=20,
        )

        assert response.status_code == 401

    def test_failed_authentication_wrong_token(self, token, input_data):

        # Alter the last token char to have an erroneous
        chunks = token.split(".")
        chunks[1] = chunks[1][:-1] + chr(ord(chunks[1][-1]) + 1)
        token = ".".join(chunks)

        response = requests.post(
            PREDICT_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            json=input_data,
            timeout=20,
        )

        assert response.status_code == 401

    def test_failed_authentication_missing_token(self, input_data):

        response = requests.post(
            PREDICT_URL,
            headers={
                "Content-Type": "application/json",
            },
            json=input_data,
            timeout=20,
        )

        assert response.status_code == 401
