from wtforms import (TextAreaField, SubmitField, HiddenField)

from lamby.forms.base import BaseForm


class ReadMeForm(BaseForm):
    markdown = TextAreaField()
    project_id = HiddenField()
    submit = SubmitField()
