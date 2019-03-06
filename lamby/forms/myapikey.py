from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class MyApiKeyForm(FlaskForm):
    api_key = StringField('API Key')
    generate_new_key = SubmitField('Generate New Key')
