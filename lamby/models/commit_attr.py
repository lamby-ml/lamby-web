from lamby.database import db


class CommitAttr(db.Model):
    # -------------------------------------------------------------------------
    # Meta
    # -------------------------------------------------------------------------
    __tablename__ = 'commit_attr'

    # -------------------------------------------------------------------------
    # Fields
    # -------------------------------------------------------------------------
    id = db.Column(db.Integer, primary_key=True)

    commit_id = db.Column(
        db.String(64),
        db.ForeignKey('commits.id'),
        nullable=False
    )

    # KEY -- Type of the attribute (eg. 'tag' or 'github-commit-hash')
    key = db.Column(db.String(50), nullable=False)

    # VALUE -- Text to associate with the key (eg. 'release 0.1.2')
    value = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return f'<CommitAttribute key={self.key} value={self.value} />'
