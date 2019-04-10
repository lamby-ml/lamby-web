from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from lamby.database import db
from lamby.forms.profile import (
    DeleteAccountForm, MyApiKeyForm, MyInfoForm, NewProjectForm
)
from lamby.models.project import Project
from lamby.models.user import User

profile_blueprint = Blueprint('profile', __name__)


@profile_blueprint.route('/')
@login_required
def index():
    return render_template(
        'profile.jinja',
        owner=current_user,
        projects=current_user.projects,
        my_info_form=MyInfoForm(),
        my_api_key_form=MyApiKeyForm(),
        delete_account_form=DeleteAccountForm(),
        new_project_form=NewProjectForm(),
        focused_tab='projects'
    )


@profile_blueprint.route('/my_info', methods=['POST'])
@login_required
def handle_my_info_form():
    my_info_form = MyInfoForm()

    if my_info_form.validate_on_submit():
        current_user.set_password(my_info_form.new_password.data)
        db.session.commit()
        flash('The change to your account was successful.', category='success')
        return redirect(url_for('profile.index'))

    return render_template(
        'profile.jinja',
        owner=current_user,
        projects=current_user.projects,
        my_info_form=my_info_form,
        my_api_key_form=MyApiKeyForm(),
        delete_account_form=DeleteAccountForm(),
        new_project_form=NewProjectForm(),
        focused_tab='info'
    )


@profile_blueprint.route('/my_api_key', methods=['POST'])
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


@profile_blueprint.route('/delete_account', methods=['POST'])
@login_required
def handle_delete_account():
    delete_account_form = DeleteAccountForm()

    if delete_account_form.validate_on_submit():
        user = User.query.filter(User.id == current_user.id).one()
        db.session.delete(user)
        db.session.commit()
        flash('You have successfully deleted your account!', category='success')
        return redirect(url_for('auth.login'))

    # Attempted to generate a new api key, but something went wrong
    flash('Something went wrong! Please try again later.', category='danger')
    return redirect(url_for('profile.index'))


@profile_blueprint.route('/new_project', methods=['POST'])
@login_required
def create_new_project():
    new_project_form = NewProjectForm()

    if new_project_form.validate_on_submit():
        project = Project(
            title=new_project_form.project_title.data,
            description=new_project_form.project_desc.data,
            owner_id=current_user.id
        )
        current_user.projects.append(project)

        db.session.add(project)
        db.session.commit()

        flash(
            'You have successfully created a new project!', category='success'
        )
        return redirect(url_for('profile.index'))

    # Attempted to generate a new api key, but something went wrong
    flash('Something went wrong! Please try again later.', category='danger')
    return redirect(url_for('profile.index'))
