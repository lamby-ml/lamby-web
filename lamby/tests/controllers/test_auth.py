from lamby.models.user import User
from lamby.tests.util import (
    get_response_data, get_response_data_without_whitespace
)


def test_signup_creates_user(test_client, test_db):
    # Should successfully create a new account
    res = test_client.post(
        '/signup',
        data=dict(
            email='test@test.com',
            password='password',
        ),
        follow_redirects=True
    )

    assert 'Lamby-Profile' in get_response_data_without_whitespace(res)
    assert User.query.filter_by(email='test@test.com').first() is not None


def test_signup_hashes_password(test_client, test_db):
    # Should successfully create a new account
    test_client.post(
        '/signup',
        data=dict(
            email='test@test.com',
            password='password',
        ),
        follow_redirects=True
    )

    user = User.query.filter_by(email='test@test.com').first()
    assert user.password != 'password'
    assert user.check_password('password')


def test_signup_requires_unique_email(test_client, test_db):
    user = User(email='test@test.com')
    user.set_password('password')
    test_db.session.add(user)
    test_db.session.commit()

    # Should fail to create duplicate account
    res = test_client.post(
        '/signup',
        data=dict(
            email='test@test.com',
            password='password',
        ),
        follow_redirects=True
    )

    assert b'Email is already in use!' in res.get_data()
    assert 'Lamby-Signup' in get_response_data_without_whitespace(res)


def test_signup_prevents_another_signup(test_client, test_db):
    # Should signup a new user with the given credentials
    res = test_client.post(
        '/signup',
        data=dict(
            email='test@test.com',
            password='password',
        ),
        follow_redirects=True
    )

    assert 'Lamby-Profile' in get_response_data_without_whitespace(res)

    # Should fail to signup a new user during an authenticated session
    res = test_client.post(
        '/signup',
        data=dict(
            email='test1@test.com',
            password='password',
        ),
        follow_redirects=True
    )

    assert 'Lamby-Profile' in get_response_data_without_whitespace(res)
    assert 'Please logout if you would like to create a ' + \
           'new account.' in get_response_data(res)
    assert User.query.filter_by(email='test1@test.com').first() is None


def test_signup_prevents_login(test_client, test_db):
    # Should signup a new user with the given credentials
    res = test_client.post(
        '/signup',
        data=dict(
            email='test@test.com',
            password='password',
        ),
        follow_redirects=True
    )

    assert 'Lamby-Profile' in get_response_data_without_whitespace(res)

    # Should fail to signup a new user during an authenticated session
    res = test_client.post(
        '/login',
        data=dict(
            email='test1@test.com',
            password='password',
        ),
        follow_redirects=True
    )

    assert 'Lamby-Profile' in get_response_data_without_whitespace(res)
    assert 'Please logout if you would like to continue as a ' + \
           'different user.' in get_response_data(res)


def test_signup_requires_password(test_client, test_db):
    # Should fail to create account with no password
    res = test_client.post(
        '/signup', data=dict(email='test@test.com', ), follow_redirects=True
    )

    assert 'Lamby-Signup' in get_response_data_without_whitespace(res)
    assert User.query.filter_by(email='test@test.com').first() is None


def test_signup_requires_email(test_client, test_db):
    # Should fail to create account with no email
    res = test_client.post(
        '/signup', data=dict(password='password', ), follow_redirects=True
    )

    assert 'Lamby-Signup' in get_response_data_without_whitespace(res)
    assert User.query.filter_by(email='test@test.com').first() is None


def test_signup_requires_valid_password(test_client, test_db):
    # Should fail to create account if password is too short
    res = test_client.post(
        '/signup',
        data=dict(email='test@test.com', password=''),
        follow_redirects=True
    )

    assert 'Lamby-Signup' in get_response_data_without_whitespace(res)
    assert User.query.filter_by(email='test@test.com').first() is None

    res = test_client.post(
        '/signup',
        data=dict(email='test@test.com', password='abc'),
        follow_redirects=True
    )

    assert 'Lamby-Signup' in get_response_data_without_whitespace(res)
    assert User.query.filter_by(email='test@test.com').first() is None


def test_login_accepts_valid_credentials(test_client, test_db):
    user = User(email='test@test.com')
    user.set_password('password')

    test_db.session.add(user)
    test_db.session.commit()

    # Should succesfully login a user with valid credentials
    res = test_client.post(
        '/login',
        data=dict(email='test@test.com', password='password'),
        follow_redirects=True
    )

    assert 'Lamby-Profile' in get_response_data_without_whitespace(res)


def test_login_rejects_nonexistent_user(test_client, test_db):
    # Should reject login attempt for non-existent user
    res = test_client.post(
        '/login',
        data=dict(email='test@test.com', password='password'),
        follow_redirects=True
    )

    assert b'Invalid Credentials!' in res.get_data()
    assert 'Lamby-Login' in get_response_data_without_whitespace(res)


def test_login_prevents_another_login(test_client, test_db):
    user = User(email='test@test.com')
    user.set_password('password')

    test_db.session.add(user)
    test_db.session.commit()

    # Should succesfully login a user with valid credentials
    res = test_client.post(
        '/login',
        data=dict(email='test@test.com', password='password'),
        follow_redirects=True
    )

    assert 'Lamby-Profile' in get_response_data_without_whitespace(res)

    # Should fail to login to a new session
    res = test_client.post(
        '/login',
        data=dict(email='test@test.com', password='password'),
        follow_redirects=True
    )

    assert 'Lamby-Profile' in get_response_data_without_whitespace(res)
    assert 'Please logout if you would like to continue as a ' + \
           'different user.' in get_response_data(res)


def test_login_prevents_signup(test_client, test_db):
    user = User(email='test@test.com')
    user.set_password('password')

    test_db.session.add(user)
    test_db.session.commit()

    # Should succesfully login a user with valid credentials
    res = test_client.post(
        '/login',
        data=dict(email='test@test.com', password='password'),
        follow_redirects=True
    )

    assert 'Lamby-Profile' in get_response_data_without_whitespace(res)

    # Should fail to login to a new session
    res = test_client.post(
        '/signup',
        data=dict(email='test@test.com', password='password'),
        follow_redirects=True
    )

    assert 'Lamby-Profile' in get_response_data_without_whitespace(res)
    assert 'Please logout if you would like to create a ' + \
           'new account.' in get_response_data(res)


def test_login_requires_email(test_client, test_db):
    # Should reject login attempt with no email
    res = test_client.post(
        '/login', data=dict(password='password'), follow_redirects=True
    )

    assert b'A valid email is required to continue.' in res.get_data()
    assert 'Lamby-Login' in get_response_data_without_whitespace(res)


def test_login_requires_valid_email(test_client, test_db):
    # Should reject login attempt for email with invalid format
    res = test_client.post(
        '/login',
        data=dict(email='invalid', password='password'),
        follow_redirects=True
    )

    assert b'A valid email is required to continue' in res.get_data()
    assert 'Lamby-Login' in get_response_data_without_whitespace(res)


def test_logout_ends_session(test_client, test_db):
    user = User(email='test@test.com')
    user.set_password('password')

    test_db.session.add(user)
    test_db.session.commit()

    # Should login the newly created user
    res = test_client.post(
        '/login',
        data=dict(email='test@test.com', password='password'),
        follow_redirects=True
    )

    assert 'Lamby-Profile' in get_response_data_without_whitespace(res)

    # Should end the user's session
    res = test_client.get('/logout', follow_redirects=True)

    assert 'Lamby-Login' in get_response_data_without_whitespace(res)

    # Should fail to access protected route after logout ends session
    res = test_client.get('/profile', follow_redirects=True)

    assert 'Please log in to access this page.' in get_response_data(res)


def test_user_change_password(test_client, test_db):
    user = User(email='test@test.com')
    user.set_password('password')

    test_db.session.add(user)
    test_db.session.commit()

    # Should login the newly created user
    test_client.post(
        '/login',
        data=dict(email='test@test.com', password='password'),
        follow_redirects=True
    )

    assert user.check_password('password')

    user.set_password('new_password')

    assert user.check_password('new_password')
