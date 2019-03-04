from flask import Blueprint, render_template
from flask_login import login_required

from lamby.util.ui import get_dummy_projects

profile_blueprint = Blueprint('profile', __name__)


@profile_blueprint.route('/', methods=['GET'])
@login_required
def index():
    return render_template('profile.jinja', projects=get_dummy_projects())
