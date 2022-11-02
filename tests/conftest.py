import tempfile

import pytest

from database.db import db
from main import app
from users.models import User


@pytest.fixture(scope="session")
def application():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["WTF_CSRF_ENABLED"] = False
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope="session")
def client(application):
    return application.test_client()


class Auth(object):
    def __init__(self, client):
        self._client = client

    def login(self, email, password):
        response = self._client.post(
            "/auth/log_in/", data={"email": email, "password": password}
        )
        return response

    def logout(self):
        return self._client.post("/auth/log_out/")


@pytest.fixture
def auth(client):
    return Auth(client)
