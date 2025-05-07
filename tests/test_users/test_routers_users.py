from http import HTTPStatus


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@example.com',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in response.json()
    assert response.json() == {
        'id': response.json()['id'],
        'username': 'testuser',
        'email': 'testuser@example.com',
    }


def test_get_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_get_users_by_id(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }


def test_update_username(client, user):
    response = client.patch(
        f'/users/username/{user.id}',
        json={'new_username': 'newusername'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['username'] == 'newusername'


def test_delete_user(client, user):
    response = client.delete(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_update_role(client, user):
    response = client.patch(f'/users/role/{user.id}/treinador')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'role': user.role}


def test_update_subscription_status(client, user):
    response = client.patch(
        f'/users/subscription_status/{user.id}',
        json={
            'id': user.id,
            'email': user.email,
            'subscription_status': 'premium',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'email': user.email,
        'subscription_status': 'premium',
    }
