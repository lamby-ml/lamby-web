from wtforms import SubmitField, HiddenField

from lamby.forms.base import BaseForm


class CreateDeploymentForm(BaseForm):
    submit = SubmitField('Deploy this Model')
    user_id = HiddenField('User ID')
    project_id = HiddenField('Project ID')
    commit_id = HiddenField('Commit ID')
