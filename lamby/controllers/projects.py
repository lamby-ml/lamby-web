import time

from flask import abort, Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user

from lamby.models.commit import Commit
from lamby.models.meta import Meta
from lamby.models.project import Project
from lamby.models.user import User
from lamby.util.ui import get_dummy_projects

projects_blueprint = Blueprint('projects', __name__)


@projects_blueprint.route('/')
def index():
    return render_template('home.jinja')


@projects_blueprint.route('/user=<int:user_id>')
def user_projects(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user == current_user:
        return redirect(url_for('profile.index'))

    if user is None:
        flash('Could not find that user!')
        return redirect(url_for('profile.index'))

    return render_template('profile.jinja', user=user_id,
                           projects=get_dummy_projects())


@projects_blueprint.route('/pid=<int:project_id>')
def project_models(project_id):

    project = Project.query.filter_by(id=project_id).first()
    # Throw 404 if no project
    if project is None:
        abort(404)
    # Query meta and pull information from there
    meta = Meta.query.filter_by(project_id=project.id)
    latest_commits = [
        Commit.query.filter_by(id=m.latest).first() for m in meta
    ]
    model_display = [
        {
            'filename': c.filename,
            'message': c.message,
            'timestamp': time.strftime(
                '%Y-%m-%d',
                time.localtime(c.timestamp)
            ),
            'link': '/models/' + str(project.id) + '/' + str(c.id)
        } for c in latest_commits
    ]
    return render_template(
        'project.jinja',
        project=model_display,
        project_title=project.title
    )
    return render_template('models.jinja', project="")
