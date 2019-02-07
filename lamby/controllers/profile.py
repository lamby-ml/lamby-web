from flask import Blueprint, render_template
from flask_login import login_required

profile_blueprint = Blueprint('profile', __name__)


@profile_blueprint.route('/', methods=['GET'])
@login_required
def index():
    return render_template('profile.jinja')
