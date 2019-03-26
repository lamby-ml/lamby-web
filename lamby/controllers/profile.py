from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from lamby.database import db
from lamby.forms.deleteaccount import DeleteAccountForm
from lamby.forms.myapikey import MyApiKeyForm
from lamby.forms.myinfo import MyInfoForm
from lamby.util.ui import get_dummy_projects

profile_blueprint = Blueprint('profile', __name__)


@profile_blueprint.route('/')
@login_required
def index():
    return render_template('profile.jinja',
                           projects=get_dummy_projects(),
                           my_info_form=MyInfoForm(),
                           my_api_key_form=MyApiKeyForm(),
                           delete_account_form=DeleteAccountForm(),
                           focused_tab='projects')


@profile_blueprint.route('/myinfo', methods=['POST'])
@login_required
def handle_my_info_form():
    my_info_form = MyInfoForm()

    if my_info_form.validate_on_submit():
        current_user.set_password(my_info_form.new_password.data)
        db.session.commit()
        flash('The change to your account was successful.', category='success')
        return redirect(url_for('profile.index'))

    return render_template('profile.jinja',
                           projects=get_dummy_projects(),
                           my_info_form=my_info_form,
                           my_api_key_form=MyApiKeyForm(),
                           delete_account_form=DeleteAccountForm(),
                           focused_tab='info')


@profile_blueprint.route('/apikey', methods=['POST'])
@login_required
def handle_my_api_key_form():
    my_api_key_form = MyApiKeyForm()

    if my_api_key_form.validate_on_submit():
        current_user.generate_new_api_key()
        db.session.commit()
        flash('A new API Key has been generated.', category='success')
        return redirect(url_for('profile.index'))

    # Attempted to generate a new api key, but something went wrong
    flash('Something went wrong! Please try again later.', category='danger')
    return redirect(url_for('profile.index'))


@profile_blueprint.route('/deleteaccount', methods=['POST'])
@login_required
def handle_delete_account():
    delete_account_form = DeleteAccountForm()

    if delete_account_form.validate_on_submit():
        current_user.delete_account()
        db.session.commit()
        flash('You have successfully deleted your account!',
              category='success')
        return redirect(url_for('auth.login'))
    # Attempted to generate a new api key, but something went wrong
    flash('Something went wrong! Please try again later.', category='danger')
    return redirect(url_for('profile.index'))
