from sqlalchemy import exc

from lamby.models.user import User


def test_user_email_is_unique(test_db):
    user = User(email='test@test.com')
    user.set_password('password')
    test_db.session.add(user)
    test_db.session.commit()

    assert User.query.filter_by(email='test@test.com').first() is not None

    try:
        user_clone = User(email='test@test.com')
        user_clone.set_password('password')
        test_db.session.add(user_clone)
        test_db.session.commit()
    except exc.IntegrityError:
        pass  # Should catch this exception
    except Exception:
        assert True is False


def test_user_password_is_hashed(test_db):
    user = User(email='test@test.com')
    user.set_password('password')
    test_db.session.add(user)
    test_db.session.commit()

    user = User.query.filter_by(email='test@test.com').first()
    assert user.password != 'password'
