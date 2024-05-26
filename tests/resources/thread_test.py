import json
from datetime import datetime
from app import db
from app.models.user import User
from app.models.thread import Thread
from app.models.comment import Comment

def create_user(name, email, password):
    return User(
        name=name,
        email=email,
        password=password,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

def create_thread(name, user_id, category=None, description=None):
    return Thread(
        name=name,
        user_id=user_id,
        category=category,
        description=description,
    )

def create_comment(thread_id, content, user_id):
    return Comment(
        thread_id=thread_id,
        content=content,
        user_id=user_id,
    )

def get_access_token(client, email, password):
    login_data = {
        'email': email,
        'password': password
    }
    response = client.post('/api/login', json=login_data)
    return json.loads(response.get_data(as_text=True)).get('access_token')

def test_create_thread(client):
    user = create_user('Test User', 'test@example.com', 'password')
    db.session.add(user)
    db.session.commit()

    access_token = get_access_token(client, 'test@example.com', 'password')
    thread_data = {
        'name': 'Sample Thread',
        'category': 'General',
        'description': 'This is a sample thread description'
    }
    response = client.post('/api/threads', headers={'Authorization': f'Bearer {access_token}'}, json=thread_data)
    response_thread = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201
    assert response_thread['name'] == 'Sample Thread'
    assert response_thread['category'] == 'General'
    assert response_thread['description'] == 'This is a sample thread description'
    assert response_thread['user_id'] == user.id

def test_get_thread(client):
    user = create_user('Test User', 'test@example.com', 'password')
    db.session.add(user)
    db.session.commit()

    access_token = get_access_token(client, 'test@example.com', 'password')
    thread = create_thread('Sample Thread', user.id, 'General', 'This is a sample thread description')
    db.session.add(thread)
    db.session.commit()

    response = client.get(f'/api/threads/{thread.id}', headers={'Authorization': f'Bearer {access_token}'})
    response_thread = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response_thread['name'] == 'Sample Thread'
    assert response_thread['category'] == 'General'
    assert response_thread['description'] == 'This is a sample thread description'
    assert response_thread['user_id'] == user.id

def test_get_threads_with_filters(client):
    user = create_user('Test User', 'test@example.com', 'password')
    db.session.add(user)
    db.session.commit()

    access_token = get_access_token(client, 'test@example.com', 'password')

    for i in range(10):
        thread = create_thread(f'Sample Thread {i}', user.id, 'General', f'This is sample thread description {i}.')
        db.session.add(thread)
    db.session.commit()

    response = client.get('/api/threads?category=General&limit=5&sort_by=created_at&order=asc&query=Sample', headers={'Authorization': f'Bearer {access_token}'})
    response_threads = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert len(response_threads) == 5

def test_update_thread(client):
    user = create_user('Test User', 'test@example.com', 'password')
    db.session.add(user)
    db.session.commit()

    access_token = get_access_token(client, 'test@example.com', 'password')
    thread = create_thread('Sample Thread', user.id, 'General', 'This is a sample thread description.')
    db.session.add(thread)
    db.session.commit()

    updated_data = {
        'name': 'Updated Thread',
        'description': 'Updated thread description'
    }
    response = client.put(f'/api/threads/{thread.id}', headers={'Authorization': f'Bearer {access_token}'}, json=updated_data)
    response_thread = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response_thread['name'] == 'Updated Thread'
    assert response_thread['description'] == 'Updated thread description'

def test_delete_thread(client):
    user = create_user('Test User', 'test@example.com', 'password')
    db.session.add(user)
    db.session.commit()

    access_token = get_access_token(client, 'test@example.com', 'password')
    thread = create_thread('Sample Thread', user.id, 'General', 'This is a sample thread description.')
    db.session.add(thread)
    db.session.commit()

    response = client.delete(f'/api/threads/{thread.id}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 204

    response = client.get(f'/api/threads/{thread.id}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 404
