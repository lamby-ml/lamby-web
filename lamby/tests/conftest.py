import os

import pytest

from lamby import create_app
from lamby.database import db
from lamby.filestore import fs


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
    if os.getenv('FLASK_ENV') != 'testing':
        raise Exception('Please set FLASK_ENV=testing before running tests.')

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
    from lamby.models.user import User

    for i in range(1, 10):
        user = User(email='test%d@test.com' % i)
        user.set_password('password')
        test_db.session.add(user)
    test_db.session.commit()
    yield User.query.all()


@pytest.fixture
def test_projects(test_db, test_users):
    from lamby.models.project import Project

    for i, user in enumerate(test_users):
        # Create a new project
        owner_id = test_users[i].id
        project = Project(title=f'Test Project {i}', owner_id=owner_id)

        # Add add members to project
        for user in test_users[0:i - 1]:
            user.projects.append(project)

        test_db.session.add(project)
    test_db.session.commit()

    yield Project.query.all()


@pytest.fixture
def test_commits(test_db, test_projects):
    import random
    import time

    from lamby.models.commit import Commit, get_dummy_hash
    from lamby.models.meta import Meta

    for i, project in enumerate(test_projects):
        # Add dummy commits to the project
        for j in range(i + 1):
            commit_id = get_dummy_hash()
            commit = Commit(
                id=commit_id,
                project_id=project.id,
                filename=f'model{j % 3}.onnx',
                message=f'Test Commit {j + 1}',
                author=f'{project.owner.email}',
                timestamp=time.time()
            )
            test_db.session.add(commit)
            test_db.session.commit()

            # Search for an existing meta for the current file
            meta = Meta.query.filter_by(
                project_id=project.id, filename=commit.filename
            ).first()

            # Create a meta if this is a new file
            if meta is None:
                meta = Meta(
                    project_id=project.id,
                    filename=commit.filename,
                    head=commit.id
                )

            # Set the head commit with a probability of 75%
            elif random.randint(0, 100) > 50:
                meta.head = commit.id

            # Update the latest commit for the current file
            meta.latest = commit.id

            test_db.session.add(meta)
            test_db.session.commit()

    yield Commit.query.all()
