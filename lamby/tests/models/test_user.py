from sqlalchemy import exc

from lamby.models.user import User
from lamby.database import db


def test_create_user(app):
    user = User(email='test@test.com', password='password')
    db.session.add(user)
    db.session.commit()

    assert User.query.filter_by(email='test@test.com').first() is not None

    try:
        user_clone = User(email='test@test.com', password='password')
        db.session.add(user_clone)
        db.session.commit()
    except exc.IntegrityError:
        pass
    except Exception:
        assert True is False
