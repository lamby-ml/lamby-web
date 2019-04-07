from wtforms import PasswordField, StringField, SubmitField, validators

from lamby.forms.base import BaseForm
from lamby.forms.validators import PasswordIsCorrect


class DeleteAccountForm(BaseForm):
    delete_account = StringField('Delete Account')
    submit = SubmitField('Delete Account')


class MyApiKeyForm(BaseForm):
    api_key = StringField('API Key')
    generate_new_key = SubmitField('Generate New Key')


class MyInfoForm(BaseForm):
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


class NewProjectForm(BaseForm):
    project_title = StringField('Project Name', validators=[
        validators.DataRequired(
            'Project name cannot be blank.'
        )
    ],)
    project_desc = StringField('Project Description')
    submit = SubmitField('Create New Project')
