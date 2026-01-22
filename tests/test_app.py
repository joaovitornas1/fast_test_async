from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_test_async.app import app


def test_root_should_return_hello():
    client = TestClient(app)

    response = client.get("/")

    assert response.json() == {"message": "Ola Mundo!"}
    assert response.status_code == HTTPStatus.OK
