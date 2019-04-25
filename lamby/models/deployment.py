from lamby.database import db


class Deployment(db.Model):
    # -------------------------------------------------------------------------
    # Meta
    # -------------------------------------------------------------------------
    __tablename__ = 'deployments'

    # -------------------------------------------------------------------------
    # Fields
    # -------------------------------------------------------------------------

    # ID -- (PrimaryKey)
    id = db.Column(db.Integer, primary_key=True)

    # Project ID -- (ForeignKey to Project)
    project_id = db.Column(
        db.Integer,
        db.ForeignKey('project.id', ondelete='CASCADE'),
        nullable=False
    )

    # Commit ID -- (ForeignKey to Commit) -- ID is hash
    commit_id = db.Column(
        db.String(64),
        db.ForeignKey('commits.id', ondelete='CASCADE'),
        nullable=False
    )

    # Deployment IP -- IP address of deployment instance
    deployment_ip = db.Column(db.String(64), nullable=False)

    # Deployment Id -- ID of digital ocean droplet instance
    droplet_id = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f'<Deployment IP={self.deployment_ip} />'

    @staticmethod
    def is_deployed(project_id, commit_id):
        return Deployment.query.filter_by(
            project_id=project_id,
            commit_id=commit_id
        ).first() is not None
