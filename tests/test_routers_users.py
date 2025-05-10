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


def test_create_user_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'password': 'testpassword',
            'email': user.email,
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


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


def test_update_password(client, user):
    response = client.patch(
        f'/users/password/{user.id}',
        json={
            'email': user.email,
            'password': 'oldpassword',
            'new_password': 'newpassword',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['id'] == user.id


def test_update_role(client, user):
    response = client.patch(f'/users/role/{user.id}/admin')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'role': 'admin'}


def test_delete_user(client, user):
    response = client.delete(f'/users/delete/{user.id}')

    assert response.status_code == HTTPStatus.NO_CONTENT


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


def test_update_nonexistent_user(client):
    response = client.patch(
        '/users/username/9999',  # ID inexistente
        json={'new_username': 'nonexistentuser'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_delete_nonexistent_user(client):
    response = client.delete('/users/delete/9999')  # ID inexistente

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_get_nonexistent_user(client):
    response = client.get('/users/9999')  # ID inexistente

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_update_subscription_status_nonexistent_user(client):
    response = client.patch(
        '/users/subscription_status/9999',  # ID inexistente
        json={
            'id': 9999,
            'email': 'nonexistent@example.com',
            'subscription_status': 'premium',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_get_users_by_email_verified_pagination(client, session, user, user_factory):
    user_factory.create_batch(10, email_verified=True)
    response = client.get('/users/email_verified/true?skip=5&limit=3')

    assert response.status_code == HTTPStatus.OK


