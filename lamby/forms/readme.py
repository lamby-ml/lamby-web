from wtforms import SubmitField, TextAreaField

from lamby.forms.base import BaseForm


class ReadMeForm(BaseForm):
    markdown = TextAreaField()
    submit = SubmitField()
