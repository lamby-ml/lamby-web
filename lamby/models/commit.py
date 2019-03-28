import hashlib

from lamby.database import db


class Commit(db.Model):
    # -------------------------------------------------------------------------
    # Meta
    # -------------------------------------------------------------------------
    __tablename__ = 'commits'

    # -------------------------------------------------------------------------
    # Fields
    # -------------------------------------------------------------------------

    # ID -- (PrimaryKey)
    id = db.Column(db.String(64), primary_key=True)

    # PROJECT_ID -- (ForeignKey to Project)
    project_id = db.Column(
        db.Integer,
        db.ForeignKey('project.id'),
        nullable=False
    )

    # FILENAME -- Name of the model tied to this commit
    filename = db.Column(db.String(120), nullable=False)

    # TIMESTAMP -- Time of the commit
    timestamp = db.Column(db.Integer)

    # MESSAGE -- Optional commit message
    message = db.Column(db.String(400))

    # AUTHOR -- User who submitted the commit
    author = db.Column(db.String(120))

    # -------------------------------------------------------------------------
    # Relationships
    # -------------------------------------------------------------------------

    # ATTRIBUTES (Commit one-to-many CommitAttr)
    # -------------------------------------------
    # Represents the attributes (eg. tags) relevant to each commit
    attributes = db.relationship('CommitAttr', backref='commit', lazy=True)

    def __str__(self):
        return f'<Commit id={self.id} message={self.message} ' + \
            f'filename={self.filename}/>'


"""
Helper functions to help generate dummy commit id's
"""


def get_dummy_hash():
    return hashlib.sha256(get_random_string(64).encode('utf-8')).hexdigest()


def get_random_string(n):
    import random
    import string

    return ''.join([random.choice(string.ascii_letters + string.digits)
                    for _ in range(n)])
