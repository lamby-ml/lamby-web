import time

import mistune

from flask import Blueprint, flash, render_template
from flask_login import login_required

from lamby.database import db

from lamby.forms.deployment import CreateDeploymentForm
from lamby.forms.projects import (EditReadmeForm, DeleteProjectForm)

from lamby.models.deployment import Deployment
from lamby.models.project import Project
from lamby.models.meta import Meta

deployment_blueprint = Blueprint('deployment', __name__)

# Collect all deployed commits for a single user and display them
@deployment_blueprint.route('/')
@login_required
def index():
    # TODO: complete template
    # will be embedded on separate page
    # deployment.jinja
    pass


# Create a new deployment instance for a model
@deployment_blueprint.route('/new_deployment/<int:project_id>',
                            methods=['POST'])
@login_required
def create_new_deployment(project_id):
    new_deployment_form = CreateDeploymentForm()

    if new_deployment_form.validate_on_submit():
        deployment = Deployment(owner_id=new_deployment_form.user_id.data,
                                project_id=new_deployment_form.project_id.data,
                                commit_id=new_deployment_form.commit_id.data,
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

    project = Project.query.get(new_deployment_form.project_id.data)

    model_table_data = [{
        'filename': commit.filename,
        'message': commit.message,
        'timestamp': time.strftime('%Y-%m-%d',
                                   time.localtime(commit.timestamp)),
        'link': f'/models/{project.id}/{commit.id}'
    } for commit in Meta.get_latest_commits(project.id)]

    markdown = mistune.Markdown()
    formatted_readme = markdown(project.readme)

    return render_template('project.jinja',
                           project=project,
                           model_table_data=model_table_data,
                           formatted_readme=formatted_readme,
                           edit_readme_form=EditReadmeForm(
                               markdown=u'' + project.readme),
                           delete_project_form=DeleteProjectForm())
