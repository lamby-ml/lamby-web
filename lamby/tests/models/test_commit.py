from sqlalchemy import exc

from lamby.models.commit import Commit, get_dummy_hash


def test_commit_with_valid_project_and_filename(test_db, test_projects):
    project = test_projects[-1]

    commit_id = get_dummy_hash()

    commit = Commit(id=commit_id, project_id=project.id, filename='model.onnx')

    test_db.session.add(commit)
    test_db.session.commit()

    assert Commit.query.get(commit_id) is not None


def test_commit_file_twice(test_db, test_projects):
    project = test_projects[-1]

    commit_id = get_dummy_hash()

    commit = Commit(id=commit_id, project_id=project.id, filename='model.onnx')

    test_db.session.add(commit)
    test_db.session.commit()

    assert Commit.query.get(commit_id) is not None

    commit_id = get_dummy_hash()

    commit = Commit(id=commit_id, project_id=project.id, filename='model.onnx')

    test_db.session.add(commit)
    test_db.session.commit()

    assert Commit.query.get(commit_id) is not None
    assert len(Commit.query.all()) == 2


def test_commmit_requires_project_id(test_db):
    commit_id = get_dummy_hash()

    try:
        commit = Commit(id=commit_id, filename='model.onnx')
        test_db.session.add(commit)
        test_db.session.commit()
    except exc.IntegrityError:
        pass  # This exception should be thrown
