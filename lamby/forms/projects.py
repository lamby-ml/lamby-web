from wtforms import SubmitField, TextAreaField

from lamby.forms.base import BaseForm


class DeleteProjectForm(BaseForm):
    submit = SubmitField('Delete Project')


class EditReadmeForm(BaseForm):
    markdown = TextAreaField()
    submit = SubmitField('Confirm Changes')
