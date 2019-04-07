from flask import Blueprint, render_template

from lamby.filestore import fs

models_blueprint = Blueprint('models', __name__)


@models_blueprint.route('/<string:project_id>/<string:commit_id>')
def model(project_id, commit_id):
    return render_template(
        'netron.jinja',
        object_link=fs.get_link(f'{project_id}/{commit_id}')
    )
