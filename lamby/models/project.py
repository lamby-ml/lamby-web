from lamby.database import db


class Project(db.Model):
    # -------------------------------------------------------------------------
    # Meta
    # -------------------------------------------------------------------------
    __tablename__ = 'project'

    # -------------------------------------------------------------------------
    # Fields
    # -------------------------------------------------------------------------

    # ID -- (PrimaryKey)
    id = db.Column(db.Integer, primary_key=True)

    # Owner ID -- (ForeignKey to User)
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False
    )

    # TITLE -- Title of the project
    title = db.Column(db.String(120), nullable=False)

    # DESCRIPTION -- Optional description of the project
    description = db.Column(db.String(240))

    # README -- Project information stored in markdown format
    readme = db.Column(db.Text, default='# README')

    # -------------------------------------------------------------------------
    # Relationships
    # -------------------------------------------------------------------------

    # COMMITS -- (Project one-to-many Commit)
    # --------------------------------------
    # Represents all of the commits for each project
    commits = db.relationship('Commit', backref='project', lazy=True)

    def __str__(self):
        return f'<Project title={self.title} description={self.description} />'
