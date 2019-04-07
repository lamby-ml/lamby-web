from flask import Blueprint, abort, redirect, render_template, url_for
from flask_login import current_user

from lamby.models.user import User

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/<int:user_id>')
def user_page(user_id):
    user = User.query.get(user_id)

    if user is None:
        abort(404)

    if user == current_user:
        return redirect(url_for('profile.index'))

    return render_template('profile.jinja', owner=user)
