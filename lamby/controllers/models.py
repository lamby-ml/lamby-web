import datetime as dt

from flask import Blueprint, flash, jsonify, redirect, render_template, url_for
from flask_login import login_required, current_user

from lamby.database import db
from lamby.filestore import fs
from lamby.models.commit import Commit
from lamby.models.deployment import Deployment
from lamby.models.meta import Meta
from lamby.models.project import Project

models_blueprint = Blueprint('models', __name__)


@models_blueprint.route('/<string:project_id>/<string:commit_id>')
def model(project_id, commit_id):
    project = Project.query.get(project_id)

    if project is None:
        flash('That project does not exist!', category='danger')
        return redirect(url_for('projects.index'))

    project = Project.query.get(project_id)
    commit = Commit.query.get(commit_id)
    author = project.owner.email
    timestamp = dt.datetime.utcfromtimestamp(
        commit.timestamp).strftime('%m-%d-%Y %I:%M %p')

    message = commit.message

    if commit is None:
        flash('That commit does not exist!', category='danger')
        return redirect(url_for('projects.index'))

    meta = Meta.query.filter_by(
        project_id=project_id,
        filename=commit.filename
    ).first()

    context = {
        'project': project,
        'commit_id': commit_id,
        'author': author,
        'timestamp': timestamp,
        'message': message,
        'commits': Commit.query.filter_by(
            project_id=project.id,
            filename=commit.filename

        ),
        'head': meta.head,
        'object_link': fs.get_link(project_id, commit_id),
        'is_deployed': Deployment.is_deployed(project_id, commit_id)
    }

    return render_template('netron.jinja', **context)


@models_blueprint.route('/change_head/<int:project_id>/<string:commit_id>',
                        methods=['POST'])
@login_required
def change_head(project_id, commit_id):
    project = Project.query.get(project_id)

    if project is None:
        flash('No such project!', category='danger')
        return jsonify({'message': 'invalid project'})

    commit = Commit.query.get(commit_id)

    if commit is None:
        flash('There was an error changing the head commit', category='danger')
        return jsonify({'message': 'invalid commit'}), 400

    meta = Meta.query.filter_by(
        project_id=project_id,
        filename=commit.filename
    ).first()

    meta.head = commit.id

    try:
        db.session.commit()
        flash(
            'You have successfully changed the head',
            category='success'
        )
    except Exception as e:
        flash('There was an error:', e)
        return jsonify({'message': 'unknown error'}), 400

    return jsonify({'message': 'success'}), 200


@models_blueprint.route('/deploy/<int:project_id>/<string:commit_id>',
                        methods=['POST'])
@login_required
def deploy_model(project_id, commit_id):
    project = Project.query.get(project_id)

    if current_user.id != project.owner_id:
        flash('Invalid user credential privilege! Unable to deploy.',
              category='danger')
        return jsonify({'message': 'invalid user'})

    if project is None:
        flash('No such project!', category='danger')
        return jsonify({'message': 'invalid project'})

    commit = Commit.query.get(commit_id)

    if commit is None:
        flash('There was an error changing the head commit', category='danger')
        return jsonify({'message': 'invalid commit'}), 400

    deploy = Deployment.query.filter_by(
        project_id=project_id,
        commit_id=commit_id
    ).first()

    if deploy is not None:
        flash('That commit is already deployed!', category='danger')
        return jsonify({'message': 'already deployed'})

    # create droplet and deploy here
    print('deploying model...')

    # TODO: remove hardcoded ip
    deploy = Deployment(
        project_id=project_id,
        commit_id=commit_id,
        deployment_ip='123.1.1.1'
    )

    db.session.add(deploy)
    db.session.commit()

    flash('Deployed Model!', category='success')
    return jsonify({'message': 'Success'})


@models_blueprint.route('/undeploy/<int:project_id>/<string:commit_id>',
                        methods=['POST'])
@login_required
def undeploy_model(project_id, commit_id):
    project = Project.query.get(project_id)

    if project is None:
        flash('No such project!', category='danger')
        return jsonify({'message': 'invalid project'}), 404

    if current_user.id != project.owner_id:
        flash(
            'Only the project owner can perform that action!',
            category='danger'
        )
        return jsonify({'message': 'invalid user'}), 401

    commit = Commit.query.get(commit_id)

    if commit is None:
        flash('This commit doesn\'t exist!', category='danger')
        return jsonify({'message': 'invalid commit'}), 400

    deploy = Deployment.query.filter_by(
        project_id=project_id,
        commit_id=commit_id
    ).first()

    if deploy is None:
        flash('That commit is not currently deployed!', category='danger')
        return jsonify({'message': 'not deployed'})

    # TODO: make call to delete droplet here
    print('deleting deployment instance...')

    db.session.delete(deploy)
    db.session.commit()

    flash('Deleted deployment!', category='success')
    return jsonify({'message': 'success'})
