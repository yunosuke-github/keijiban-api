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

def test_create_comment(client):
    user = create_user('Test User', 'test@example.com', 'password')
    db.session.add(user)
    db.session.commit()

    access_token = get_access_token(client, 'test@example.com', 'password')
    thread = create_thread('Sample Thread', user.id, 'General', 'This is a sample thread description.')
    db.session.add(thread)
    db.session.commit()

    comment_data = {
        'thread_id': thread.id,
        'content': 'This is a sample comment'
    }
    response = client.post('/api/comments', headers={'Authorization': f'Bearer {access_token}'}, json=comment_data)
    response_comment = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201
    assert response_comment['content'] == 'This is a sample comment'
    assert response_comment['thread_id'] == thread.id
    assert response_comment['user_id'] == user.id

def test_get_comment(client):
    user = create_user('Test User', 'test@example.com', 'password')
    db.session.add(user)
    db.session.commit()

    access_token = get_access_token(client, 'test@example.com', 'password')
    thread = create_thread('Sample Thread', user.id, 'General', 'This is a sample thread description.')
    db.session.add(thread)
    db.session.commit()

    comment = create_comment(thread.id, 'This is a sample comment', user.id)
    db.session.add(comment)
    db.session.commit()

    response = client.get(f'/api/comments/{comment.id}', headers={'Authorization': f'Bearer {access_token}'})
    response_comment = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response_comment['content'] == 'This is a sample comment'
    assert response_comment['thread_id'] == thread.id
    assert response_comment['user_id'] == user.id

def test_get_comments_with_filters(client):
    user = create_user('Test User', 'test@example.com', 'password')
    db.session.add(user)
    db.session.commit()

    access_token = get_access_token(client, 'test@example.com', 'password')
    thread = create_thread('Sample Thread', user.id, 'General', 'This is a sample thread description.')
    db.session.add(thread)
    db.session.commit()

    for i in range(10):
        comment = create_comment(thread.id, f'This is comment {i}.', user.id)
        db.session.add(comment)
    db.session.commit()

    response = client.get(f'/api/comments?thread_id={thread.id}&limit=5&sort_by=created_at&order=asc', headers={'Authorization': f'Bearer {access_token}'})
    response_comments = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert len(response_comments) == 5

def test_update_comment(client):
    user = create_user('Test User', 'test@example.com', 'password')
    db.session.add(user)
    db.session.commit()

    access_token = get_access_token(client, 'test@example.com', 'password')
    thread = create_thread('Sample Thread', user.id, 'General', 'This is a sample thread description.')
    db.session.add(thread)
    db.session.commit()

    comment = create_comment(thread.id, 'This is a sample comment.', user.id)
    db.session.add(comment)
    db.session.commit()

    updated_data = {
        'content': 'Updated comment content'
    }
    response = client.put(f'/api/comments/{comment.id}', headers={'Authorization': f'Bearer {access_token}'}, json=updated_data)
    response_comment = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response_comment['content'] == 'Updated comment content'

def test_delete_comment(client):
    user = create_user('Test User', 'test@example.com', 'password')
    db.session.add(user)
    db.session.commit()

    access_token = get_access_token(client, 'test@example.com', 'password')
    thread = create_thread('Sample Thread', user.id, 'General', 'This is a sample thread description.')
    db.session.add(thread)
    db.session.commit()

    comment = create_comment(thread.id, 'This is a sample comment.', user.id)
    db.session.add(comment)
    db.session.commit()

    response = client.delete(f'/api/comments/{comment.id}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 204

    response = client.get(f'/api/comments/{comment.id}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 404
