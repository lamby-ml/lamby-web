from lamby.models.commit import Commit
from lamby.models.meta import Meta


def test_meta_get_filenames(test_db, test_projects, test_commits):
    project = test_projects[-1]

    meta_filenames = Meta.get_filenames(project.id)

    all_filenames = list(set([commit.filename for commit in project.commits]))

    assert len(meta_filenames) == len(all_filenames)

    for file in all_filenames:
        assert file in meta_filenames


def test_meta_get_head_commits(test_db, test_projects, test_commits):
    project = test_projects[-1]

    head_commits = Meta.get_head_commits(project.id)

    all_filenames = list(set([commit.filename for commit in project.commits]))

    assert len(head_commits) == len(all_filenames)

    for commit in head_commits:
        assert Commit.query.get(commit) is not None


def test_meta_get_latest_commits(test_db, test_projects, test_commits):
    project = test_projects[-1]

    latest_meta_commits = Meta.get_latest_commits(project.id)

    # Fetch actual latest commits
    latest_commits = Commit.query.filter_by(
        project_id=project.id
    ).order_by(Commit.timestamp.desc()).limit(len(latest_meta_commits))

    for commit in latest_meta_commits:
        assert Commit.query.get(commit) in latest_commits
