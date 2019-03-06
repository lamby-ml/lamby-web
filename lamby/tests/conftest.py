import pytest

from lamby import create_app
from lamby.database import db
from lamby.filestore import fs
from lamby.models.user import User


@pytest.fixture
def test_client(scope='module'):
    """
    Create and configure an isolated app instance for each test.
    """
    app = create_app()
    client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture
def test_db(test_client, scope='module'):
    """
    Setup an in-memory database for each test, then tear it down after each
    test is complete.
    """
    db.create_all()
    db.session.commit()

    yield db

    db.drop_all()


@pytest.fixture
def test_fs(test_client, scope='module'):
    yield fs
    fs.clear_testing_bucket()


@pytest.fixture
def test_users(test_db):
    for i in range(1, 10):
        user = User(email='test%d@test.com' % i)
        user.set_password('password')
        test_db.session.add(user)
    test_db.session.commit()
    yield User.query.all()
