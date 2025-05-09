from http import HTTPStatus


def test_get_info_user(client):
    response = client.get('/detail/')

    assert response.status_code == HTTPStatus.OK
    assert 'details' in response.json()
    assert isinstance(response.json()['details'], list)
    assert len(response.json()['details']) >= 0


def test_get_info_user_with_pagination(client):
    response = client.get('/detail/?skip=0&limit=10')

    assert response.status_code == HTTPStatus.OK
    assert 'details' in response.json()
    assert isinstance(response.json()['details'], list)


def test_get_info_user_by_id(client, user_details):
    response = client.get(f'/detail/{user_details.id}')

    assert response.status_code == HTTPStatus.OK


def test_get_info_user_by_id_not_found(client):
    response = client.get('/detail/9999')  # ID inexistente

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Informações não encontrado'}


def test_update_info_user(client, user_details):
    update_data = {
        'id': user_details.id,
        'user_id': user_details.user_id,
        'altura': 1.75,
        'data_de_nascimento': '2000-01-01',
    }

    response = client.patch('/detail/', json=update_data)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user_details.id,
        'user_id': user_details.user_id,
    }


def test_update_info_user_invalid_data(client, user_details):
    update_data = {
        'id': user_details.id,
        'user_id': user_details.user_id,
        'altura': 'invalid',  # Dado inválido
        'data_de_nascimento': '2000-01-01',
    }

    response = client.patch('/detail/', json=update_data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert 'detail' in response.json()


def test_update_info_user_picture(client, user_details):
    update_data = {
        'user_id': user_details.user_id,
        'profile_picture_url': 'https://example.com/new_picture.jpg',
    }

    response = client.patch('/detail/picture', json=update_data)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user_details.id,
        'user_id': user_details.user_id,
        'profile_picture_url': update_data['profile_picture_url'],
    }


def test_update_info_user_picture_not_found(client):
    update_data = {
        'user_id': 9999,  # ID inexistente
        'profile_picture_url': 'https://example.com/nonexistent_picture.jpg',
    }

    response = client.patch('/detail/picture', json=update_data)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Informações não encontrado'}
