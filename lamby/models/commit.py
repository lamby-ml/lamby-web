from lamby.database import db


class Commit(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey(
        'project.id'), primary_key=True)
    timestamp = db.Column(db.Integer)
    message = db.Column(db.String(400))
    author = db.Column(db.String(120))

    def __str__(self):
        return '<Commit id=%s message=%s />' % \
            (self.id, self.message)
