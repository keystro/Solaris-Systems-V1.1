import pytest
from main import main as flask_app

@pytest.fixture
def app():
    yeild flask_app

@pytest.fixture
def client(app):
    return app.test_client()
