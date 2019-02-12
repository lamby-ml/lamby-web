import pytest

from lamby import create_app
from lamby.database import db


@pytest.fixture
def app():
    """
    Create and configure an isolated app instance for each test.
    """
    app = create_app()

    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture
def client(app):
    """
    Create a test client for the application.
    """
    return app.test_client()
