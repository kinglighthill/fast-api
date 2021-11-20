import pytest
from jose import jwt
from app import schemas
from app.config import settings


def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == 'Hello World'
    assert res.status_code == 200


def test_create_user(client):
    email = "hello@gmail.com"
    res = client.post(
        "/users", json={
            "email": email,
            "password": "1234"
        }
    )
    response = schemas.UserResponse(**res.json())
    assert response.data.email == email
    assert res.status_code == 201


def test_login_user(test_user, client):
    res = client.post(
        "/login", data={
            "username": test_user['email'],
            "password": test_user['password']
        }
    )
    login_res = schemas.TokenResponse(**res.json())
    payload = jwt.decode(login_res.data.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.data.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('email', '1234', 403),
    ('hello@gmail.com', 'password', 403),
    ('email', 'password', 403),
    (None, '1234', 422),
    ('hello@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={
            "username": email,
            "password": password
        }
    )
    
    assert res.status_code == status_code
    # assert res.json()['message'] == "Invalid Credentials"