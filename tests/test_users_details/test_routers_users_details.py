from http import HTTPStatus


def test_get_info_user(client):
    response = client.get('/detail/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'details': []}


def test_get_info_user_by_id(client, user_details):
    response = client.get(f'/detail/{user_details.id}')

    assert response.status_code == HTTPStatus.OK
