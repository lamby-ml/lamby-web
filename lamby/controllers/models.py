from flask import Blueprint, flash, jsonify, redirect, render_template, url_for
from flask_login import login_required

from lamby.database import db
from lamby.filestore import fs
from lamby.models.commit import Commit
from lamby.models.meta import Meta
from lamby.models.project import Project

models_blueprint = Blueprint('models', __name__)


@models_blueprint.route('/<string:project_id>/<string:commit_id>')
def model(project_id, commit_id):
    project = Project.query.get(project_id)

    if project is None:
        flash('That project does not exist!', category='danger')
        return redirect(url_for('projects.index'))

    commit = Commit.query.get(commit_id)

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
        'commits': Commit.query.filter_by(
            project_id=project.id,
            filename=commit.filename
        ),
        'head': meta.head,
        'object_link': fs.get_link(project_id, commit_id),
    }

    return render_template('netron.jinja', **context)


@models_blueprint.route('change_head/<int:project_id>/<string:commit_id>',
                        methods=['POST'])
@login_required
def change_head(project_id, commit_id):
    commit = Commit.query.get(commit_id)

    if commit is None:
        flash('There was an error changing the head commit', category='danger')
        return None, 400

    meta = Meta.query.filter_by(project_id=project_id,
                                filename=commit.filename).first()

    if meta is None:
        flash('There was an error reseting the head')
        return jsonify({'message': 'fail'}), 400
    else:
        meta.head = commit.id
        try:
            db.session.commit()
            flash(
                'You have successfully reset the head',
                category='success'
            )
        except Exception as e:
            flash('There was an error:', e)
            return jsonify({'message': 'fail'}), 400

    return jsonify({'message': 'nice'}), 200
