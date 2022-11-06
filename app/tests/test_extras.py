from http import HTTPStatus


def test_contact_page(client):
    response = client.get("/contact-us/")
    assert response.status_code == HTTPStatus.OK
    assert b"Get in touch" in response.data


def test_about_us_page(client):
    response = client.get("/about/")
    assert response.status_code == HTTPStatus.OK
    assert b"About us" in response.data
