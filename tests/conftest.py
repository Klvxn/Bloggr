import tempfile

import pytest
from database.db import db
from main import app
from users.models import User


@pytest.fixture(scope="session")
def application():
    app.config["TESTING"] = True
    _, path = tempfile.mkstemp()

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["DATABASE"] = path
    app.config["WTF_CSRF_ENABLED"] = False
    print(app.config["DATABASE"])
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
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
