import os

from flask import Blueprint, abort, render_template

from lamby.filestore import fs
from lamby.models.commit import Commit

deploy_blueprint = Blueprint('deploy', __name__)


@deploy_blueprint.route('/<commit_id>')
def deploy(commit_id):
    commit = Commit.query.get(commit_id)

    if commit is None:
        abort(404)

    return render_template(
        'deploy.jinja',
        commit=commit,
        token=os.getenv('DIGITAL_OCEAN_API_KEY'),
        link=fs.get_link(f'{commit.project_id}/{commit.id}')
    )
