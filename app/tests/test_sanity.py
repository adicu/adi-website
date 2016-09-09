import mongoengine


def test_create_app(app):
    assert app.config["TESTING"]
    assert app.config["CSRF_ENABLED"]
    assert mongoengine.connection.get_db().name == "testing"
