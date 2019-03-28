def test_api_projects_clone(test_client, test_projects, test_commits):
    res = test_client.get(f'/api/projects/{test_projects[-1].id}')
    json = res.json

    assert json['commits'] is not None
    assert json['heads'] is not None
    assert json['latest_commits'] is not None


def test_api_projects_push_status(test_client, test_users, test_projects,
                                  test_commits):
    # Generate an API token for a user
    user = test_projects[-1].members[0]
    user.generate_new_api_key()
