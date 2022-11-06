import os
from pathlib import Path

import pytest
from database.db import db
from main import app as test_app


@pytest.fixture(scope="session")
def application():
    base_dir = Path(__file__).resolve().cwd()
    test_app.config["TESTING"] = True
    test_db = "app/database/tests.db"
    test_app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{Path(base_dir).joinpath(test_db)}"
    test_app.config["WTF_CSRF_ENABLED"] = False

    db.init_app(test_app)

    with test_app.app_context():
        db.create_all()
        yield test_app
        db.drop_all()
    os.unlink(test_db)


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
