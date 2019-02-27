from lamby.database import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(240))

    def __str__(self):
        return '<Project title=%s description=%s />' % \
            (self.title, self.description)
