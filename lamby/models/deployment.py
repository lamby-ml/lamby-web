from lamby.database import db


class Deployment(db.Model):
    # -------------------------------------------------------------------------
    # Meta
    # -------------------------------------------------------------------------
    __tablename__ = 'deployment'

    # -------------------------------------------------------------------------
    # Fields
    # -------------------------------------------------------------------------
    # ID -- (PrimaryKey)
    id = db.Column(db.Integer, primary_key=True)

    # Owner ID -- (ForeignKey to User)
    owner_id = db.Column(db.Integer,
                         db.ForeignKey('user.id', ondelete='CASCADE'),
                         nullable=False)

    # Project ID -- (ForeignKey to Project)
    project_id = db.Column(db.Integer,
                           db.ForeignKey('project.id', ondelete='CASCADE'),
                           nullable=False)

    # Commit ID -- (ForeignKey to Commit) -- ID is hash
    commit_id = db.Column(db.String(64),
                          db.ForeignKey('commit.id', ondelete='CASCASE'),
                          nullable=False)

    # Deployment IP -- IP address of deployment instance
    deployment_ip = db.Column(db.String(64), nullable=False)

    def __str__(self):
        return f'< Deployment IP={self.deployment_ip}/>'
