from http import HTTPStatus


def test_register(client):
    data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@bloggr.com",
        "about": "I am a backend developer with python",
        "password": "Testingwithflask123",
        "password2": "Testingwithflask123",
    }
    response = client.post("/auth/register/", data=data, follow_redirects=True)
    assert response.status_code == HTTPStatus.OK
    assert b"Registration was successful" in response.data


def test_login_user(client):
    data = {
        "email": "testuser@bloggr.com",
        "password": "Testingwithflask123",
    }
    response = client.post(
        "/auth/log_in/",
        data=data,
        follow_redirects=True,
    )
    assert b"You are logged in successfully" in response.data


def test_logout(client):
    response = client.post("/auth/log_out/", follow_redirects=True)
    assert response.status_code == HTTPStatus.OK
    assert b"You are now logged out" in response.data


def test_change_password(client, auth):
    auth.login("testuser@bloggr.com", "Testingwithflask123")
    data = {
        "old_password": "Testingwithflask123",
        "new_password": "TestingwithPytest321",
        "new_password2": "TestingwithPytest321",
    }
    # Other tests would require the new password to log in
    response = client.post(
        "/auth/change_password/",
        data=data,
        follow_redirects=True,
    )
    assert b"Password changed succesfully" in response.data
