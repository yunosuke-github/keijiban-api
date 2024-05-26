from .. import db


class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(10), nullable=True)
    description = db.Column(db.String(400), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    views = db.Column(db.Integer, default=0)
    deleted = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('threads', lazy=True))

    def __init__(self, name, user_id, category=None, description=None):
        self.name = name
        self.category = category
        self.description = description
        self.user_id = user_id
