"""
To run this file run:
flask shell
> from lamby.database.stub import stub
> stub()
"""

import random
import time

from lamby.database import db
from lamby.models.commit import Commit, get_dummy_hash
from lamby.models.meta import Meta
from lamby.models.project import Project
from lamby.models.user import User


def stub():
    for i in range(1, 10):
        user = User(email='test%d@test.com' % i)
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

    test_users = User.query.all()

    for i, user in enumerate(test_users):
        # Create a new project
        owner_id = test_users[i].id
        project = Project(title=f'Test Project {i}', owner_id=owner_id)

        # Add add members to project
        for user in test_users[0:i-1]:
            user.projects.append(project)
        db.session.add(project)

    test_projects = Project.query.all()

    for i, project in enumerate(test_projects):
        # Add dummy commits to the project
        for j in range(i+1):
            commit_id = get_dummy_hash()
            commit = Commit(id=commit_id, project_id=project.id,
                            filename=f'model{j % 3}.onnx',
                            message=f'Test Commit {j + 1}',
                            author=f'{project.owner.email}',
                            timestamp=time.time())
            db.session.add(commit)

            # Search for an existing meta for the current file
            meta = Meta.query.filter_by(project_id=project.id,
                                        filename=commit.filename).first()

            # Create a meta if this is a new file
            if meta is None:
                meta = Meta(project_id=project.id,
                            filename=commit.filename, head=commit.id)

            # Set the head commit with a probability of 75%
            elif random.randint(0, 100) > 50:
                meta.head = commit.id

            # Update the latest commit for the current file
            meta.latest = commit.id
            db.session.add(meta)

    db.session.commit()
