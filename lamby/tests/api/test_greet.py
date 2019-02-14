from flask import url_for


def test_api_greet(test_client):
    res = test_client.get(url_for('greet.index'))
    assert res.json == {'message': 'Hello, World!'}
