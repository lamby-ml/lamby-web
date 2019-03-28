def test_api_projects_clone(test_client, test_projects, test_commits):
    res = test_client.get(f'/api/projects/{test_projects[-1].id}')
    json = res.json

    assert json['commits'] is not None
    assert json['heads'] is not None
    assert json['latest_commits'] is not None
