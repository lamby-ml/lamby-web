from wtforms import StringField, SubmitField

from lamby.forms.base import BaseForm


class DeleteAccountForm(BaseForm):
    delete_account = StringField('Delete Account')
    submit = SubmitField('Delete Account')
