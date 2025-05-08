from http import HTTPStatus


def test_get_info_user(client):
    response = client.get('/detail/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'details': []}


def test_get_info_user_by_id(client, user_details):
    response = client.get(f'/detail/{user_details.id}')

    assert response.status_code == HTTPStatus.OK


def test_update_info_user(client, user_details):
    update_data = {
        'id': user_details.id,
        'user_id': user_details.user_id,
        'altura': 1.75,
        'data_de_nascimento': '2000-01-01',
    }

    response = client.patch('/detail/', json=update_data)

    assert response.status_code == HTTPStatus.OK


def test_update_user_is_activo(client, user_details):
    update_data = {
        'id': user_details.id,
        'user_id': user_details.user_id,
        'is_active': False,
    }

    response = client.patch('/detail/', json=update_data)

    assert response.status_code == HTTPStatus.OK