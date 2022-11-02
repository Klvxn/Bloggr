from http import HTTPStatus


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert b"There are currently no blogs yet." in response.data


def test_add_blog(client, auth):
    """
    Test a authenticated users can post a blog
    while unauthenticated users will be redirected to age
    """
    client.post("/auth/log_out/")
    data = {
        "title": "Testing A Flask Blog Application With Pytest",
        "content": "Read the Pytest documentation and you'd know how to run tests with pytest.",
        "tag": "tests",
    }
    get_response = client.get("/add_new_blog/", follow_redirects=True)
    assert get_response.status_code == HTTPStatus.OK
    assert b"Please log in to access this page" in get_response.data

    auth.login("testuser@bloggr.com", "TestingwithPytest321")
    post_response = client.post(
        "/add_new_blog/",
        data=data,
        follow_redirects=True,
    )
    assert post_response.status_code == HTTPStatus.OK
    assert b"Blog posted successfully" in post_response.data


def test_get_single_blog(client):
    response = client.post("/blogs/1/")
    assert response.status_code == HTTPStatus.OK


def test_edit_blog(client):
    data = {
        "title": "Testing A Flask Blog Application With Pytest",
        "content": "Read the Pytest documentation and you'd know how to run tests with pytest.",
        "tag": "Test with Pytest, Flask",
    }
    response = client.post(
        "/blogs/1/edit_blog/",
        data=data,
        follow_redirects=True,
    )
    assert response.status_code == HTTPStatus.OK
    assert b"Update was saved successfully" in response.data


def test_delete_blog(client):
    response = client.post("/blogs/1/delete_blog/", follow_redirects=True)
    assert response.status_code == HTTPStatus.OK
    assert b"Your blog has been deleted" in response.data
