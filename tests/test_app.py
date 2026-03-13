# pyright: basic
from http import HTTPStatus



def test_root_should_return_hello(client):
    response = client.get("/")
    assert response.json() == {"message": "Ola Mundo!"}
    assert response.status_code == HTTPStatus.OK


def test_health_check_return_html(client):
    response = client.get("/health_check")

    assert response.status_code == HTTPStatus.OK
    assert "<h1> Olá </h1>" in response.text


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "alice",
            "email": "example@github.com",
            "password": "12345",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "email": "example@github.com",
        "username": "alice",
    }


def test_read_users(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "id": 1,
                "email": "example@github.com",
                "username": "alice",
            }
        ]
    }


def test_read_user(client):
    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "email": "example@github.com",
        "username": "alice",
    }


def test_read_user_err(client):
    response = client.get("/users/0")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User Not Found"}


def test_update_user(client):
    response = client.put(
        "/users/1",
        json={
            "id": 1,
            "email": "alice_test@github.com",
            "username": "alice",
            "password": "NEWTEST",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "email": "alice_test@github.com",
        "username": "alice",
    }


def test_update_user_err(client):
    response = client.put(
        "/users/0",
        json={
            "id": 0,
            "email": "test@github.com",
            "username": "test",
            "password": "test",
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User Not Found"}


def test_delete_user(client):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"operation": "Successfully"}


def test_delete_user_not_found(client):
    response = client.delete("/users/0")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User Not Found"}
