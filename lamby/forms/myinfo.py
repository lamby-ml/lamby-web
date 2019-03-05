from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, validators

from lamby.forms.validators import PasswordIsCorrect


class MyInfoForm(FlaskForm):
    email = StringField('Email')
    old_password = PasswordField(
        'Password',
        validators=[
            PasswordIsCorrect(
                message='Old Password does not match current password'
            ),
        ],
    )
    new_password = PasswordField(
        'Password',
        validators=[
            validators.DataRequired(
                'A valid password is required to continue.'
            ),
            validators.Length(
                min=5,
                max=50,
                message='Password must be between 5 and 50 characters long.'
            )
        ],
    )
    submit = SubmitField('Change Password')
