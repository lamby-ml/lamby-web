import secrets

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from lamby.database import db
from lamby.models.projects import projects


class User(UserMixin, db.Model):
    # -------------------------------------------------------------------------
    # Meta
    # -------------------------------------------------------------------------
    __tablename__ = 'user'

    # -------------------------------------------------------------------------
    # Fields
    # -------------------------------------------------------------------------

    # ID -- (PrimaryKey)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # EMAIL -- Unique email of the user
    email = db.Column(db.String(120), unique=True, nullable=False)

    # PASSWORD -- Encrypted password of the user
    password = db.Column(db.String(120), nullable=False)

    # API_KEY -- Token that gives the user access to push and pull from the cli
    api_key = db.Column(db.String(120))

    # -------------------------------------------------------------------------
    # Relationships
    # -------------------------------------------------------------------------

    # OWNED_PROJECTS (USER one-to-many PROJECT)
    # -----------------------------------------
    # Represents the projects that the user owns/created
    owned_projects = db.relationship(
        'Project',
        backref='owner',
        lazy=True,
        cascade='all,delete-orphan'
    )

    # PROJECTS (User many-to-many Project)
    # ------------------------------------
    # Represents the projects where the user is a member
    projects = db.relationship(
        'Project',
        secondary=projects,
        lazy='subquery',
        backref=db.backref('members', lazy=True),
        cascade='all,delete'
    )

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_new_api_key(self):
        self.api_key = secrets.token_urlsafe(32)

    def __str__(self):
        return f'<User email={self.email} />'
