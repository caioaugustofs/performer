from http import HTTPStatus

from fastapi.testclient import TestClient

from performer.app import app


def test_hello():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Ola, bem-vindo ao Performer!'
        ' Para acessar a API, use /docs ou /redoc'
    }


def test_health():
    client = TestClient(app)

    response = client.get('/health')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'status': 'ok'}
