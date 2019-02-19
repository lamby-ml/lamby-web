from flask import Blueprint, flash, redirect, render_template, url_for

from lamby.models.user import User
from lamby.util.ui import get_dummy_projects

projects_blueprint = Blueprint('projects', __name__)


@projects_blueprint.route('/')
def index():
    return render_template('home.jinja')


@projects_blueprint.route('/<int:user_id>')
def user_projects(user_id):
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        flash('Could not find that user!')
        return redirect(url_for('profile.jinja'))

    return render_template('profile.jinja', projects=get_dummy_projects())
