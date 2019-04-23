import time
import mistune

from flask import Blueprint, flash, render_template, redirect, url_for, abort
from flask_login import login_required, current_user

from lamby.database import db
from lamby.forms.deployment import CreateDeploymentForm
from lamby.models.deployment import Deployment
from lamby.models.project import Project
from lamby.models.meta import Meta
from lamby.models.commit import Commit

from lamby.forms.projects import (EditReadmeForm, DeleteProjectForm)

deployment_blueprint = Blueprint('deployment', __name__)

# Collect all deployed commits for a single user and display them
@deployment_blueprint.route('/')
@login_required
def index():
    deployments = Deployment.query.filter_by(owner_id=current_user.id)
    deployments_data = []

    for deployment in deployments:
        project = Project.query.get(deployment.project_id)
        commit = Commit.query.get(deployment.commit_id)
        entry = {
            'id': deployment.id,
            'project_name': project.title,
            'file_name': commit.filename,
            'commit_hash': commit.id[0:5]
        }
        deployments_data.append(entry)

    return render_template('deployments.jinja',
                           deployment_data=deployments_data)


@deployment_blueprint.route('/<int:deployment_id>')
@login_required
def deployment(deployment_id):
    deployment = Deployment.query.get(deployment_id)

    if deployment is None:
        abort(404)

    return render_template('deployment.jinja')


# Create a new deployment instance for a model
@deployment_blueprint.route('/new_deployment/' +
                            '<int:project_id>/<string:commit_id>',
                            methods=['POST'])
@login_required
def create_new_deployment(project_id, commit_id):
    new_deployment_form = CreateDeploymentForm()

    if new_deployment_form.validate_on_submit():
        deployment = Deployment(owner_id=current_user.id,
                                project_id=project_id,
                                commit_id=commit_id,
                                deployment_ip='TEMP')

        # TODO: make call to deploy model here
        print("making call to deployment service...")
        db.session.add(deployment)
        db.session.commit()
        flash('You successfully requested to deploy a model! Check back here'
              + ' to see the deployment status of your model.',
              category='success')
    else:
        flash('Unable to deploy model, please try again later.',
              category='failure')

    project = Project.query.get(project_id)
    model_table_data = [{
        'filename': commit.filename,
        'message': commit.message,
        'timestamp': time.strftime('%Y-%m-%d',
                                   time.localtime(commit.timestamp)),
        'link': f'/models/{project.id}/{commit.id}',
        'is_deployed': Deployment.is_deployed(project_id, commit.id)
    } for commit in Meta.get_latest_commits(project.id)]

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


@deployment_blueprint.route('/delete/<int:deployment_id>')
@login_required
def delete_deployment(deployment_id):
    deployment = Deployment.query.get(deployment_id)

    if current_user.id == deployment.owner_id:
        db.session.delete(deployment)
        db.session.commit()

        flash('Successfully depleted deployment instance. ',
              category='success')

    else:
        flash('You must be this deployment\'s owner in order to delete it.',
              category='failure')

    return redirect(url_for('deployment.index'))
