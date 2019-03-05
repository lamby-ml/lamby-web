from flask import Blueprint, flash, render_template, request
from flask_login import current_user, login_required

from lamby.database import db
from lamby.forms.myinfo import MyInfoForm
from lamby.util.ui import get_dummy_projects

profile_blueprint = Blueprint('profile', __name__)


@profile_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index():
    my_info_form = MyInfoForm()

    if my_info_form.validate_on_submit():
        current_user.set_password(my_info_form.new_password.data)
        db.session.commit()
        flash('The change to your account was successful.', category='success')
        return render_template('profile.jinja',
                               projects=get_dummy_projects(),
                               my_info_form=my_info_form,
                               focused_tab='projects')
    elif request.method == 'POST':
        # Attempted to change password, but form was invalid
        return render_template('profile.jinja',
                               projects=get_dummy_projects(),
                               my_info_form=my_info_form,
                               focused_tab='info')

    return render_template('profile.jinja', projects=get_dummy_projects(),
                           my_info_form=my_info_form, focused_tab='projects')
