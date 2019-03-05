from flask_login import current_user
from wtforms import ValidationError


class PasswordIsCorrect(object):
    def __init__(self, message='Invalid Password'):
        self.message = message

    def __call__(self, form, field):
        if not current_user.check_password(field.data or ''):
            raise ValidationError(self.message)
