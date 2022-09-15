import pytest
from api.index import app


@pytest.fixture()
def api():
    yield app


@pytest.fixture()
def client(api):
    return api.test_client()
