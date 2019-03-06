from sqlalchemy import exc

from lamby.models.project import Project


def test_project_accepts_valid_owner(test_db, test_users):
    project = Project(title='Test Project',
                      description='A project for testing purposes',
                      owner_id=test_users[0].id)

    test_db.session.add(project)
    test_db.session.commit()

    assert Project.query.filter_by(id=project.id).first() is not None


def test_project_rejects_empty_owner(test_db):
    try:
        project = Project(title='Test Project',
                          description='A project for testing purposes')
        test_db.session.add(project)
        test_db.session.commit()
        raise Exception
    except exc.IntegrityError:
        pass  # Should cach this exception
    except Exception:
        raise
