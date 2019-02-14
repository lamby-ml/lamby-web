import pytest

from lamby import create_app
from lamby.database import db


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
