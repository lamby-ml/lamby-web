from wtforms import StringField, SubmitField

from lamby.forms.base import BaseForm


class MyApiKeyForm(BaseForm):
    api_key = StringField('API Key')
    generate_new_key = SubmitField('Generate New Key')
