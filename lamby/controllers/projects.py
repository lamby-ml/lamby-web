import time

import mistune
from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user

from lamby.database import db
from lamby.forms.deployment import CreateDeploymentForm
from lamby.forms.projects import DeleteProjectForm, EditReadmeForm
from lamby.models.meta import Meta
from lamby.models.project import Project
from lamby.models.deployment import Deployment

projects_blueprint = Blueprint('projects', __name__)


@projects_blueprint.route('/')
def index():
    projects = Project.query.limit(10).all()
    return render_template('projects.jinja', projects=projects)


@projects_blueprint.route('/<int:project_id>')
def project(project_id):
    project = Project.query.get(project_id)

    if project is None:
        abort(404)

    model_table_data = [{
        'filename': commit.filename,
        'message': commit.message,
        'timestamp': time.strftime('%Y-%m-%d',
                                   time.localtime(commit.timestamp)),
        'link': f'/models/{project.id}/{commit.id}',
        'commit_id': commit.id,
        'is_deployed': Deployment.is_deployed(project_id, commit.id)
    }for commit in Meta.get_latest_commits(project.id)]

    markdown = mistune.Markdown()
    formatted_readme = markdown(project.readme)

    return render_template('project.jinja',
                           project=project,
                           model_table_data=model_table_data,
                           formatted_readme=formatted_readme,
                           edit_readme_form=EditReadmeForm(
                               markdown=u'' + project.readme),
                           delete_project_form=DeleteProjectForm(),
                           create_deployment_form=CreateDeploymentForm())


@projects_blueprint.route('/readme/<int:project_id>', methods=['POST'])
def handle_edit_readme(project_id):
    edit_readme_form = EditReadmeForm()

    if edit_readme_form.validate_on_submit():
        project = Project.query.get(project_id)
        project.readme = edit_readme_form.markdown.data

        db.session.commit()

        flash('Successfully updated README.', category='success')
        return redirect(url_for('projects.project', project_id=project_id))

    flash('Unable to update README.', category='failure')
    return redirect(url_for('projects.project', project_id=project_id))


@projects_blueprint.route('/delete/<int:project_id>', methods=['POST'])
def handle_delete_project(project_id):
    delete_project_form = DeleteProjectForm()

    if delete_project_form.validate_on_submit():
        project = Project.query.get(project_id)

        current_user.projects.remove(project)
        current_user.owned_projects.remove(project)

        db.session.delete(project)
        db.session.commit()

        flash('You have successfully delete the project!', category='success')
        return redirect(url_for('profile.index'))

    flash('Something went wrong! Please try again later.', category='danger')
    return redirect(url_for('profile.index'))
