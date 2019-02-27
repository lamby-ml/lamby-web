from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from lamby.database import db
from lamby.models.projects import projects


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    projects = db.relationship('Project', secondary=projects, lazy='subquery',
                               backref=db.backref('members', lazy=True))

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __str__(self):
        return '<User email=%s />' % self.email
