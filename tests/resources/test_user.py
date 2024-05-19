from app import db
from app.models.user import User
import json


def test_get_users(client):
    user = User(name='Test User', email='test@example.com')
    db.session.add(user)
    db.session.commit()

    response = client.get('/api/users')
    response_user = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response_user[0]['name'] == 'Test User'
    assert response_user[0]['email'] == 'test@example.com'


def test_get_user(client):
    user = User(name='Test User', email='test@example.com')
    db.session.add(user)
    db.session.commit()
    user_id = user.id

    response = client.get(f'/api/users/{user_id}')
    response_user = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response_user['name'] == 'Test User'
    assert response_user['email'] == 'test@example.com'


def test_post_user(client):
    user_data = {'name': 'New User', 'email': 'new@example.com'}
    response = client.post('/api/users', json=user_data)
    response_user = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201
    assert response_user['name'] == 'New User'
    assert response_user['email'] == 'new@example.com'


def test_put_user(client):
    user = User(name='Test User', email='test@example.com')
    db.session.add(user)
    db.session.commit()
    user_id = user.id

    updated_data = {'name': 'Updated User'}
    response = client.put(f'/api/users/{user_id}', json=updated_data)
    response_user = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response_user['name'] == 'Updated User'
    assert response_user['email'] == 'new@example.com'


def test_delete_user(client):
    user = User(name='Test User', email='test@example.com')
    db.session.add(user)
    db.session.commit()
    user_id = user.id

    response = client.delete(f'/api/users/{user_id}')
    assert response.status_code == 204

    response = client.get(f'/api/users/{user_id}')
    assert response.status_code == 404
