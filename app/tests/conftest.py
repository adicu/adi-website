import pytest


@pytest.yield_fixture(scope="session")
def app():
    from .. import create_app
    yield create_app()
