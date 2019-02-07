from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from lamby.database import db
from lamby.forms.auth import AuthForm
from lamby.models.user import User

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('profile.index'))

    form = AuthForm()
    form.submit.label.text = 'SIGNUP'

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first() is not None:
            flash('Email is already in use!', category='danger')
            return redirect(url_for('auth.signup'))

        user = User(email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        login_user(user, remember=True)
        return redirect(url_for('profile.index'))

    return render_template('auth.jinja', is_signup=True, form=form)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile.index'))

    form = AuthForm()
    form.submit.label.text = 'LOGIN'

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid Credentials!', category='danger')
            return redirect(url_for('auth.login'))

        login_user(user, remember=True)
        return redirect(url_for('profile.index'))

    return render_template('auth.jinja', is_signup=False, form=form)


@auth_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
