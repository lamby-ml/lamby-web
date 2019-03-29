from wtforms import StringField, SubmitField, validators

from lamby.forms.base import BaseForm


class NewProjectForm(BaseForm):
    project_title = StringField('Project Name', validators=[
        validators.DataRequired(
            'Project name cannot be blank.'
        )
    ],)
    project_desc = StringField('Project Description')
    submit = SubmitField('Create New Project')
