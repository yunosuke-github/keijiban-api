from werkzeug.security import generate_password_hash

from .. import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), index=True, unique=False, nullable=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(120), index=True, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime)

    def __init__(self, name, email, password, created_at=None, updated_at=None):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.created_at = created_at
        self.updated_at = updated_at
