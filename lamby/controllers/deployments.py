from flask import Blueprint, flash, url_for
from flask_login import login_required

from lamby.database import db
from lamby.forms.deployment import CreateDeploymentForm
from lamby.models.deployment import Deployment

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

    return url_for('projects.project', project_id=project_id)
