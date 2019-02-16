from lamby.models.user import User
from lamby.tests.util import get_response_data_without_whitespace


def test_signup_creates_user(test_client, test_db, scope='module'):
    # Should successfully create a new account
    res = test_client.post('/signup', data=dict(
        email='test@test.com',
        password='password',
    ), follow_redirects=True)

    assert 'Lamby-Profile' in get_response_data_without_whitespace(res)
    assert User.query.filter_by(email='test@test.com').first() is not None


def test_signup_requires_unique_email(test_client, test_db, scope='module'):
    user = User(email='test@test.com')
    user.set_password('password')
    test_db.session.add(user)
    test_db.session.commit()

    # Should fail to create duplicate account
    res = test_client.post('/signup', data=dict(
        email='test@test.com',
        password='password',
        remember_me=False,
    ), follow_redirects=True)

    assert b'Email is already in use!' in res.get_data()
    assert 'Lamby-Signup' in get_response_data_without_whitespace(res)


def test_signup_requires_password(test_client, test_db):
    # Should fail to create account with no password
    res = test_client.post('/signup', data=dict(
        email='test@test.com',
    ), follow_redirects=True)

    assert 'Lamby-Signup' in get_response_data_without_whitespace(res)
    assert User.query.filter_by(email='test@test.com').first() is None


def test_signup_requires_email(test_client, test_db):
    # Should fail to create account with no email
    res = test_client.post('/signup', data=dict(
        password='password',
    ), follow_redirects=True)

    assert 'Lamby-Signup' in get_response_data_without_whitespace(res)
    assert User.query.filter_by(email='test@test.com').first() is None


def test_signup_requires_valid_password(test_client, test_db):
    # Should fail to create account if password is too short
    res = test_client.post('/signup', data=dict(
        email='test@test.com',
        password=''
    ), follow_redirects=True)

    assert 'Lamby-Signup' in get_response_data_without_whitespace(res)
    assert User.query.filter_by(email='test@test.com').first() is None

    res = test_client.post('/signup', data=dict(
        email='test@test.com',
        password='abc'
    ), follow_redirects=True)

    assert 'Lamby-Signup' in get_response_data_without_whitespace(res)
    assert User.query.filter_by(email='test@test.com').first() is None


def test_login_accepts_valid_credentials(test_client, test_db):
    user = User(email='test@test.com')
    user.set_password('password')
    test_db.session.add(user)
    test_db.session.commit()

    # Should succesfully login a user with valid credentials
    res = test_client.post('/login', data=dict(
        email='test@test.com',
        password='password'
    ), follow_redirects=True)

    assert 'Lamby-Profile' in get_response_data_without_whitespace(res)


def test_login_rejects_nonexistent_user(test_client, test_db):
    # Should reject login attempt for non-existent user
    res = test_client.post('/login', data=dict(
        email='test@test.com',
        password='password'
    ), follow_redirects=True)

    assert b'Invalid Credentials!' in res.get_data()
    assert 'Lamby-Login' in get_response_data_without_whitespace(res)
