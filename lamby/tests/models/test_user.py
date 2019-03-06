from sqlalchemy import exc

from lamby.models.project import Project
from lamby.models.user import User


def test_user_creation(test_db):
    user = User(email='test@test.com')
    user.set_password('password')

    test_db.session.add(user)
    test_db.session.commit()

    assert User.query.filter_by(email='test@test.com').first() is not None


def test_user_requires_unique_email(test_db):
    user = User(email='test@test.com')
    user.set_password('password')

    test_db.session.add(user)
    test_db.session.commit()

    try:
        user_clone = User(email='test@test.com')
        user_clone.set_password('password')
        test_db.session.add(user_clone)
        test_db.session.commit()
        raise Exception
    except exc.IntegrityError:
        pass  # Should catch this exception
    except Exception:
        raise


def test_user_set_password(test_db):
    user = User(email='test@test.com')
    user.set_password('password')
    test_db.session.add(user)
    test_db.session.commit()

    user = User.query.filter_by(email='test@test.com').first()
    assert user.password != 'password'


def test_user_check_password(test_db):
    user = User(email='test@test.com')
    user.set_password('password')

    assert user.check_password('password')


def test_user_can_access_owned_projects(test_db, test_users):
    user = test_users[0]

    project = Project(title='Test Project',
                      description='A project for testing purposes',
                      owner_id=test_users[0].id)

    test_db.session.add(project)
    test_db.session.commit()

    assert Project.query.filter_by(id=project.id).first() in \
        user.owned_projects


def test_user_generate_new_api_key(test_db, test_users):
    user = test_users[0]

    assert user.api_key is None

    user.generate_new_api_key()

    assert user.api_key is not None

    old_key = user.api_key
    user.generate_new_api_key()

    assert user.api_key != old_key
