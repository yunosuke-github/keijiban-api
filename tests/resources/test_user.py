import json
from datetime import datetime
from app import db
from app.models.user import User

def create_user(name, email, password):
    return User(
        name=name,
        email=email,
        password=password,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

def get_access_token(client, email, password):
    login_data = {
        'email': email,
        'password': password
    }
    response = client.post('/api/login', json=login_data)
    return json.loads(response.get_data(as_text=True)).get('access_token')

def test_create_user(client):
    user_data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password'
    }
    response = client.post('/api/users', json=user_data)
    response_user = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201
    assert response_user['name'] == 'Test User'
    assert response_user['email'] == 'test@example.com'

def test_get_user(client):
    user = create_user('Test User', 'test@example.com', 'password')
    db.session.add(user)
    db.session.commit()

    access_token = get_access_token(client, 'test@example.com', 'password')
    response = client.get(f'/api/users/{user.id}', headers={'Authorization': f'Bearer {access_token}'})
    response_user = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response_user['name'] == 'Test User'
    assert response_user['email'] == 'test@example.com'

def test_update_user(client):
    user = create_user('Test User', 'test@example.com', 'password')
    db.session.add(user)
    db.session.commit()

    access_token = get_access_token(client, 'test@example.com', 'password')
    updated_data = {
        'name': 'Updated User'
    }
    response = client.put(f'/api/users/{user.id}', headers={'Authorization': f'Bearer {access_token}'}, json=updated_data)
    response_user = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response_user['name'] == 'Updated User'

def test_delete_user(client):
    user = create_user('Test User', 'test@example.com', 'password')
    db.session.add(user)
    db.session.commit()

    access_token = get_access_token(client, 'test@example.com', 'password')
    response = client.delete(f'/api/users/{user.id}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 204

    response = client.get(f'/api/users/{user.id}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 404
