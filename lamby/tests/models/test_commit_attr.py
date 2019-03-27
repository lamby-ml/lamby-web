from lamby.models.commit_attr import CommitAttr


def test_commit_attr_add_tag(test_db, test_commits):
    commit = test_commits[0]

    tag = CommitAttr(key='tag', value='testing')
    commit.attributes.append(tag)

    test_db.session.add(tag)
    test_db.session.commit()
