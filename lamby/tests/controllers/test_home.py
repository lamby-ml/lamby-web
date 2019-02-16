from lamby.tests.util import get_response_data_without_whitespace


def test_index(test_client):
    res = test_client.get('/')
    assert 'Hello,Anon!' in get_response_data_without_whitespace(res)
