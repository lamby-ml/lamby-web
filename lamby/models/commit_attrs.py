from lamby.database import db


class CommitAttrs(db.Model):
    commit_id = db.Column(db.String(64), db.ForeignKey(
        'commit.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey(
        'project.id'), primary_key=True)
    key = db.Column(db.String(50), primary_key=True)
    value = db.Column(db.String(50))

    def __str__(self):
        return '<CommitAttribute key=%s value=%s />' % \
            (self.key, self.value)
