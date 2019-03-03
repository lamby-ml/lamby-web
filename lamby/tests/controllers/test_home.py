from lamby.tests.util import get_response_data


def test_index(test_client, test_db, scope='module'):
    res = test_client.get('/')
    assert 'Popular Projects' in get_response_data(res)
