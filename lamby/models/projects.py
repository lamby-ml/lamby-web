from lamby.database import db

projects = db.Table(
    'projects',
    db.Column('user_id',
              db.Integer,
              db.ForeignKey('user.id', ondelete='CASCADE'),
              primary_key=True),
    db.Column('project_id',
              db.Integer,
              db.ForeignKey('project.id'),
              primary_key=True),
)
