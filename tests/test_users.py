from http import HTTPStatus


def test_get_a_users_page(client):
    response = client.get("/users/1/")
    assert response.status_code == HTTPStatus.OK
    assert b"My Account" in response.data


def test_update_user_account(client, auth):
    auth.login("testuser@bloggr.com", "TestingwithPytest321")
    data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "flasktestuser@bloggr.com",
        "about": "I am a backend developer with Python and also a student at AltSchool Africa",
    }
    response = client.post(
        "/users/1/update_my_account/",
        data=data,
        follow_redirects=True,
    )
    assert response.status_code == HTTPStatus.OK
    assert b"Update was saved successfully" in response.data


def test_delete_user_account(client, auth):
    # Log in the test_user using the updated email address and password
    auth.login("flasktestuser@bloggr.com", "TestingwithPytest321")
    response = client.post("/users/1/delete_account/", follow_redirects=True)
    assert response.status_code == HTTPStatus.OK
    assert b"Your account has been deleted" in response.data
