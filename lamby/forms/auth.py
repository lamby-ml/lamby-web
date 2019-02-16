from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField
from wtforms import validators


class AuthForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            validators.DataRequired('A valid email is required to continue.'),
            validators.Email('A valid email is required to continue.'),
        ],
    )
    password = PasswordField(
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
    remember_me = BooleanField('Remember')
    submit = SubmitField('Submit')
