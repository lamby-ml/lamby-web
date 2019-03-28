from flask import Blueprint, render_template

from lamby.filestore import fs

model_blueprint = Blueprint('model', __name__)


@model_blueprint.route('/<string:pid>/<string:mid>')
def index(pid, mid):
    return render_template(
        'netron.jinja',
        object_link=fs.get_link(str(id) + '/' + str(mid))
    )
