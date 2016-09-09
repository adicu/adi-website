import pytest


@pytest.yield_fixture(scope="function")
def client(app):
    yield app.test_client()


@pytest.yield_fixture(scope="function")
def admin_session(client):
    with client.session_transaction() as session:
        session["gplus_id"] = "admin123"
        yield session


@pytest.mark.parametrize("url", [
    "/", "/events", "/resources", "/labs", "/blog", "/contact",
])
def test_client_routes_ok(client, url):
    assert client.get(url).status_code == 200


@pytest.mark.parametrize("url", ["/events/15", "/blog/15"])
def test_client_routes_redirect(client, url):
    assert client.get(url).status_code == 302


@pytest.mark.parametrize("url", [
    "/admin/media", "/admin/events/create", "/admin/posts/new", "/admin/home",
    "/admin/events", "admin/posts", "/admin/users",
])
def test_admin_routes_ok(client, admin_session, url):
    assert client.get(url).status_code == 200


def test_admin_routes_redirect(client, admin_session):
    assert client.get("/admin").status_code == 301
    assert client.get("/admin/users/me").status_code == 302
