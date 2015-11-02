"""
.. module:: base
    :synopsis: This defines common functionality in our test suite, in the base
    class :class:`TestingTemplate`, which should be inherited by all test
    suite classes.

.. moduleauthor:: Dan Schlosser <dan@danrs.ch>
"""

import unittest
import os
import mongoengine
from coverage import coverage
from app import create_app
from config.flask_config import config

USERS = {
    'user': {
        'name': 'Test User',
        'email': 'user@te.st',
        'user_type': 'fake_user',
        'gplus_id': 'user123'
    },
    'editor': {
        'name': 'Test Editor',
        'email': 'editor@te.st',
        'user_type': 'editor',
        'gplus_id': 'editor123'
    },
    'publisher': {
        'name': 'Test Publisher',
        'email': 'publisher@te.st',
        'user_type': 'publisher',
        'gplus_id': 'publisher123'
    },
    'admin': {
        'name': 'Test Admin',
        'email': 'admin@te.st',
        'user_type': 'admin',
        'gplus_id': 'admin123'
    }
}


class TestingTemplate(unittest.TestCase):

    def setUp(self):  # noqa
        """Before every test, make some example users."""
        from eventum.models import User
        for user_config in USERS.values():
            user = User(**user_config)
            user.save()

    def tearDown(self):  # noqa
        """After every test, delete users created in :func:`setUp`."""
        from eventum.models import User
        User.drop_collection()

    @classmethod
    def setUpClass(cls):  # noqa
        """Sets up a test database before each set of tests."""
        cls.app = create_app(
            MONGODB_SETTINGS={'DB': 'testing'},
            TESTING=True,
            CSRF_ENABLED=False,
            WTF_CSRF_ENABLED=False
        )
        from eventum.models import User
        User.drop_collection()

    def request_with_role(self, path, method='GET', role='admin',
                          *args, **kwargs):
        """Make an http request with the given role's gplus_id
        in the session and a User with the given role in the database.
        """
        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                if role in USERS:
                    # if it isn't, the request is without a role
                    sess['gplus_id'] = USERS[role]['gplus_id']
                kwargs['method'] = method
                kwargs['path'] = path
            return c.open(*args, **kwargs)

    def test_create_test_app(self):
        """Assert that we are in a proper testing environment."""
        self.assertTrue(self.app.config['TESTING'])
        self.assertFalse(self.app.config['CSRF_ENABLED'])
        self.assertEqual(mongoengine.connection.get_db().name, 'testing')

    @classmethod
    def main(cls):
        cov = coverage(
            branch=True, omit=['test.py', 'test/*', 'lib/*',
                               'include/*', 'bin/*'])
        cov.start()
        try:
            unittest.main()
        except:
            pass
        cov.stop()
        cov.save()
        print "\n\nCoverage Report:\n"
        cov.report()
        print "HTML version: " + \
            os.path.join(config['BASEDIR'], "tmp/coverage/index.html")
        cov.html_report(directory='tmp/coverage')
        cov.erase()


if __name__ == '__main__':
    TestingTemplate.main()
