"""
.. module:: test_routes
    :synopsis: This module tests that routes behaive as expected in Eventum.

.. moduleauthor:: Dan Schlosser <dan@danrs.ch>
"""

from base import TestingTemplate


class TestRoutes(TestingTemplate):
    """Test the basic behavior of routes in eventum."""

    OK = (200, 201)
    REDIRECT = (301, 302)

    CLIENT_ROUTE_EXPECTATIONS = [
        ('/', OK),
        ('/events', OK),
        ('/events/15', REDIRECT),
        ('/resources', OK),
        ('/labs', OK),
        ('/blog', OK),
        ('/blog/15', REDIRECT),
        ('/contact', OK),
    ]

    EVENTUM_ROUTE_EXPECTATIONS = [
        ('/admin', REDIRECT),
        ('/admin/home', OK),
        ('/admin/events', OK),
        ('/admin/events/create', OK),
        ('/admin/posts', OK),
        ('/admin/posts/new', OK),
        ('/admin/users', OK),
        ('/admin/users/me', REDIRECT),
        ('/admin/media', OK),
    ]

    ROUTE_MSG = 'Error requesting route: {}. {} not in {}.'

    def test_client_routes(self):
        """Test that routes on the client return the expected status codes."""
        for url, code in self.CLIENT_ROUTE_EXPECTATIONS:
            response = self.request_with_role(url)
            self.assertIn(response.status_code,
                          code,
                          msg=self.ROUTE_MSG.format(url,
                                                    response.status_code,
                                                    code))

    def test_eventum_routes(self):
        """Test that routes in Eventum return the expected status codes."""
        for url, code in self.EVENTUM_ROUTE_EXPECTATIONS:
            response = self.request_with_role(url, role='admin')
            self.assertIn(response.status_code,
                          code,
                          msg=self.ROUTE_MSG.format(url,
                                                    response.status_code,
                                                    code))
