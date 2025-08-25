import pytest
import requests

from tests.constants import LOGIN_URL


@pytest.fixture(scope="function")
def credentials():
    return {"username": "user123", "password": "password123"}


@pytest.fixture(scope="function")
def token(credentials):
    r = requests.post(url=LOGIN_URL, json={"credentials": credentials}, timeout=1)
    if r.status_code != 200:
        raise ValueError("Impossible to login")
    return r.json()["access_token"]


@pytest.fixture(scope="function")
def input_data():
    return {
        "input_data": {
            "university_rating": 3,
            "sop": 1,
            "lor": 4.5,
            "cgpa": 9.5,
            "research": True,
        }
    }
