import pytest

from lamby import create_app


@pytest.fixture
def app():
    """
    Create and configure an isolated app instance for each test.
    """
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    """
    Create a test client for the application.
    """
    return app.test_client()
