from wtforms import HiddenField, SubmitField

from lamby.forms.base import BaseForm


class CreateDeploymentForm(BaseForm):
    submit = SubmitField('Deploy this Model')
    user_id = HiddenField('User ID')
