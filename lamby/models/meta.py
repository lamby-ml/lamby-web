from lamby.database import db


class Meta(db.Model):
    # -------------------------------------------------------------------------
    # Meta
    # -------------------------------------------------------------------------
    __tablename__ = 'meta'

    # -------------------------------------------------------------------------
    # Fields
    # -------------------------------------------------------------------------

    # PROJECT_ID -- (PrimaryKey, ForeignKey to Project)
    project_id = db.Column(
        db.Integer,
        db.ForeignKey('project.id'),
        primary_key=True
    )

    # FILENAME  -- (PrimaryKey) -- Name of the model for the project
    filename = db.Column(db.String(64), nullable=False, primary_key=True)

    # LATEST -- (ForeignKey to Commit) -- Latest Commit id for the model
    latest = db.Column(
        db.String(64),
        db.ForeignKey('commits.id'),
        nullable=False
    )

    # HEAD -- (ForeignKey to Commit) -- CommitID for the head commit
    head = db.Column(
        db.String(64),
        db.ForeignKey('commits.id'),
        nullable=False
    )

    def __str__(self):
        return f'<Meta filename={self.filename} latest={self.latest}' + \
            f' head={self.head} />'

    @staticmethod
    def get_filenames(project_id):
        return [meta.filename for meta in
                Meta.query.filter_by(project_id=project_id)]

    @staticmethod
    def get_head_commits(project_id):
        return [meta.head for meta in
                Meta.query.filter_by(project_id=project_id)]

    @staticmethod
    def get_latest_commits(project_id):
        return [meta.latest for meta in
                Meta.query.filter_by(project_id=project_id)]
