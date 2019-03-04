from lamby.models.user import User
from lamby.tests.util import (get_response_data,
                              get_response_data_without_whitespace)


def test_profile_is_accessible_to_authenticated_user(test_client, test_db):
    user = User(email='test@test.com')
    user.set_password('password')
    test_db.session.add(user)
    test_db.session.commit()

    # Should successfully authenticate the user
    test_client.post('/login', data=dict(
        email='test@test.com',
        password='password'
    ), follow_redirects=True)

    # Should successfully go to profile page
    res = test_client.get('/profile')

    assert 'Lamby-Profile' in get_response_data_without_whitespace(res)


def test_profile_is_blocked_for_unauthenticated_user(test_client, test_db):
    # Should fail to authenticate
    test_client.post('/login', data=dict(
        email='invalid_user@test.com',
        password='invalid'
    ), follow_redirects=True)

    # Should redirect to login page
    res = test_client.get('/profile', follow_redirects=True)

    assert 'Please log in to access this page.' in get_response_data(res)


def test_profile_more_info(test_client, test_db):
    user = User(email='test@test.com')
    user.set_password('password')
    test_db.session.add(user)
    test_db.session.commit()

    # Should successfully authenticate the user
    test_client.post('/login', data=dict(
        email='test@test.com',
        password='password'
    ), follow_redirects=True)

    # Should go to profile page
    res = test_client.get('/profile', follow_redirects=True)

    assert 'value="test@test.com"' in get_response_data(res)
    assert 'value="1"' in get_response_data(res)
