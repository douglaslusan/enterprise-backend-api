from tests.conftest import client
import uuid


def test_login_success():

    unique_email = f"{uuid.uuid4()}@gmail.com"

    client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": unique_email,
            "password": "123456",
            "role": "user"
        }
    )

    response = client.post(
        "/users/login",
        data={
            "username": unique_email,
            "password": "123456"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data


def test_login_invalid():

    response = client.post(
        "/users/login",
        data={
            "username": "wrong@gmail.com",
            "password": "wrong"
        }
    )

    assert response.status_code == 401