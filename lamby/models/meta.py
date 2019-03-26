from lamby.database import db


class ProjectMeta(db.Model):
    project_id = db.Column(db.Integer, db.ForeignKey(
        'project.id'), primary_key=True)
    filename = db.Column(db.String(120), primary_key=True)
    head = db.Column(db.String(64), db.ForeignKey('commit.id'))
    latest = db.Column(db.String(64), db.ForeignKey('commit.id'))

    def __str__(self):
        return '<ProjectMetadata file=%s head=%s latest=%s/>' % \
            (self.filename, self.head, self.latest)
