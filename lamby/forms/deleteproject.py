from wtforms import StringField, SubmitField

from lamby.forms.base import BaseForm


class DeleteProjectForm(BaseForm):
    proj_id = StringField('Project Id')
    submit = SubmitField('Delete Project')
