from flask import flash
from flask_wtf import FlaskForm


class BaseForm(FlaskForm):
    def _flash_errors(self):
        for field, errors in self.errors.items():
            for error in errors:
                flash('%s' % error, category='danger')
        return False

    def validate_on_submit(self):
        return True if super().validate_on_submit() else \
            self._flash_errors()
