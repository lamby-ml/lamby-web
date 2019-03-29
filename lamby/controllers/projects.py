import time

import mistune
from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user

from lamby.database import db
from lamby.forms.deleteproject import DeleteProjectForm
from lamby.forms.readme import ReadMeForm
from lamby.models.meta import Meta
from lamby.models.project import Project
from lamby.models.user import User

markdown = mistune.Markdown()
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

    return render_template('home.jinja', projects=user.projects,
                           scope=user.email)


@projects_blueprint.route('/pid=<int:project_id>')
def project_models(project_id):
    project = Project.query.filter_by(id=project_id).first()

    # Throw 404 if no project
    if project is None:
        abort(404)

    latest_commits = Meta.get_latest_commits(project.id)

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

    md = markdown(project.read_me)

    return render_template(
        'project.jinja',
        project=model_display,
        project_title=project.title,
        project_id=project_id,
        readme_edit_form=ReadMeForm(markdown=u''+project.read_me),
        delete_project_form=DeleteProjectForm(),
        read_me=project.read_me,
        mark_up=md,
        owner_id=int(project.owner_id)
    )


@projects_blueprint.route('/edit_readme/<int:project_id>', methods=['POST'])
def edit_readme_form(project_id):
    edit_readme_form = ReadMeForm()

    if edit_readme_form.validate_on_submit():
        project = Project.query.get(project_id)
        project.read_me = edit_readme_form.markdown.data
        db.session.commit()
        flash('Successfully updated README.', category='success')
        return redirect(url_for('projects.project_models',
                                project_id=project_id))

    flash('Unable to update README.', category='failure')
    return redirect(url_for('projects.project_models',
                            project_id=project_id))


@projects_blueprint.route('/deleteproject/<int:project_id>', methods=['POST'])
def handle_delete_project(project_id):
    delete_project_form = DeleteProjectForm()

    if delete_project_form.validate_on_submit():
        project = Project.query.get(project_id)
        current_user.projects.remove(project)
        current_user.owned_projects.remove(project)
        db.session.delete(project)
        db.session.commit()
        flash('You have successfully delete the project!',
              category='success')
        return redirect(url_for('profile.index'))

    flash('Something went wrong! Please try again later.', category='danger')
    return redirect(url_for('profile.index'))
