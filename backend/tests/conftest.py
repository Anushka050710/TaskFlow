import pytest
from app import create_app
from app.config import TestConfig
from app.database import db as _db


@pytest.fixture(scope="session")
def app():
    app = create_app(TestConfig)
    return app


@pytest.fixture(scope="function")
def client(app):
    with app.app_context():
        _db.create_all()
        yield app.test_client()
        _db.session.remove()
        _db.drop_all()
