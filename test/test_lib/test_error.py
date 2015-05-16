"""
.. module:: test_error
    :synopsis: Tests for the :mod:`~app.lib.error` module.

.. moduleauthor:: Dan Schlosser <dan@danrs.ch>
"""
from test.base import TestingTemplate
from app.lib.error import EventumError, _ERROR_DATA


class TestErrorMethods(TestingTemplate):
    """Test the date, time, and datetime formatting in the Event model."""

    def setUp(self):  # noqa
        """Disable logging, as we don't want logging to be outputted during
        the tests.  Without this, any instantiations of EventumError subclasses
        would log.
        """
        self.app.logger.disabled = True

    def tearDown(self):  # noqa
        """Re-enable logging."""
        self.app.logger.propagate = False

    def test_namespaced_error_is_properly_subclassed(self):
        """An error should be a subclass of all of the errors that it is
        namespaced underneath.
        """
        err = EventumError.GCalAPI.NotFound.UpdateFellBackToCreate()
        err_class = err.__class__
        self.assertTrue(issubclass(err_class, EventumError.GCalAPI.NotFound))
        self.assertTrue(issubclass(err_class, EventumError.GCalAPI))
        self.assertTrue(issubclass(err_class, EventumError))

    def test_error_data_is_assigned(self):
        """An error should have been assigned an appropriate ``message``,
        ``error_code``, ``http_status_code``.
        """
        err = EventumError.GCalAPI.NotFound.UpdateFellBackToCreate()
        message, error_code, http_status_code, _ = (
            _ERROR_DATA['GCalAPI'][3]['NotFound'][3]['UpdateFellBackToCreate']
        )
        self.assertEqual(err.message, message)
        self.assertEqual(err.error_code, error_code)
        self.assertEqual(err.http_status_code, http_status_code)

    FORM_MESSAGE_MSG = ('EventumError._form_message() failed:\n'
                        'expected: {}\n'
                        '     got: {}\n')
    FORM_MESSAGE_EXPECTATIONS = [
        ('Error at url `%s`: %s', ('/home', 'Not Found'),
         'Error at url `/home`: Not Found'),
        ('Error at url `%s`: %s', ('/home',),
         'Error at url `/home`: '),
        ('Error at url.', ('/home',),
         'Error at url.')
    ]

    def test_form_message(self):
        """Test that :func:`EventumError._form_message()` returns the expected
        output when given too few, too many, or the right number of subs.
        """
        error = EventumError()
        for message, subs, expected_output in self.FORM_MESSAGE_EXPECTATIONS:
            output = error._form_message(message, subs)
            self.assertEqual(output,
                             expected_output,
                             msg=self.FORM_MESSAGE_MSG.format(expected_output,
                                                              output))
