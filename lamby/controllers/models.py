from flask import Blueprint, flash, render_template, jsonify
from flask_login import login_required

from lamby.database import db
from lamby.filestore import fs
from lamby.models.commit import Commit
from lamby.models.meta import Meta
from lamby.models.project import Project

models_blueprint = Blueprint('models', __name__)


@models_blueprint.route('/<string:project_id>/<string:commit_id>')
def model(project_id, commit_id):
    project_owner_id = Project.query.filter_by(id=project_id).first().owner.id
    commit = Commit.query.filter_by(id=commit_id)
    meta_head = Meta.query.filter_by(project_id=project_id,
                                     filename=commit[0].filename).first().head
    return render_template(
        'netron.jinja',
        object_link=fs.get_link(f'{project_id}/{commit_id}'),
        commits=Commit.query.filter_by(
            project_id=project_id, filename=commit[0].filename),
        project_id=project_id,
        project_owner_id=project_owner_id,
        current_commit=commit_id,
        head_commit=meta_head)


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
            flash('You have successfully reset the head',
                  category='success')
        except Exception as e:
            flash('There was an error:', e)
            return jsonify({'message': 'fail'}), 400

    return jsonify({'message': 'nice'}), 200
