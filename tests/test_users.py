from tests.conftest import client
import uuid


def test_create_user():

    unique_email = f"{uuid.uuid4()}@gmail.com"

    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": unique_email,
            "password": "123456",
            "role": "user"
        }
    )

    assert response.status_code == 200