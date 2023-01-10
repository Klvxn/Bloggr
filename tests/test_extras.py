from http import HTTPStatus


def test_contact_page(client):
    response = client.get("/contact-us/")
    assert response.status_code == HTTPStatus.OK
    assert b"Get in touch" in response.data


def test_send_message(client):
    data = {
        "name": "Flask user",
        "email": "flaskuser@bloggr.com",
        "message": "This is a test"
    }
    response = client.post("/contact-us/", data=data, follow_redirects=True)
    assert response.status_code == HTTPStatus.OK
    assert b"Your message was sent successfully" in response.data


def test_about_us_page(client):
    response = client.get("/about/")
    assert response.status_code == HTTPStatus.OK
    assert b"Welcome to Bloggr" in response.data
