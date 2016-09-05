"""
.. module:: test_event
    :synopsis: Tests for the :class:`~app.models.Event` model.

.. moduleauthor:: Dan Schlosser <dan@danrs.ch>
"""
from test.base import TestingTemplate
from datetime import date, time


class TestModelEvent(TestingTemplate):
    """Test the date, time, and datetime formatting in the Event model."""
    ERROR_MSG = 'Incorrect {}:\nexpected: "{}"\n     got: "{}".'

    EVENT_KWARGS = {
        'title': 'My Event',
        'slug': 'my-event',  # We can use the same slug because we aren't
                             # going to save the events.
        'location': '742 Evergreen Terrace',
        'short_description_markdown': 'Come to my event',
        'long_description_markdown': 'I swear, it\'ll be *great*!`',
        'is_recurring': False
    }

    DATETIMES = [
        (   # Multi-day event
            date(2015, 3, 31), time(23),
            date(2015, 4, 1), time(3),
            'Tuesday, March 31 11pm - Wednesday, April 1 3am'
        ),
        (   # Multi-day event that shares am/pm
            date(2015, 3, 31), time(23),
            date(2015, 4, 1), time(23),
            'Tuesday, March 31 11pm - Wednesday, April 1 11pm'
        ),
        (   # Single day event
            date(2015, 3, 31), time(11, 0),
            date(2015, 3, 31), time(14, 15),
            'Tuesday, March 31 11am-2:15pm'
        ),
        (   # Single day event that shares am/pm
            date(2015, 3, 31), time(15, 0),
            date(2015, 3, 31), time(19, 30),
            'Tuesday, March 31 3-7:30pm'
        ),
        (   # None start date
            None, time(23),
            date(2015, 4, 1), time(3),
            '???, ??/?? 11pm - Wednesday, April 1 3am'
        ),
        (   # None start time
            date(2015, 3, 31), None,
            date(2015, 4, 1), time(3),
            'Tuesday, March 31 ??:?? - Wednesday, April 1 3am'
        ),
        (   # None end date
            date(2015, 3, 31), time(23), None, time(3),
            'Tuesday, March 31 11pm - ???, ??/?? 3am'
        ),
        (   # None start time
            date(2015, 3, 31), time(23), date(2015, 4, 1), None,
            'Tuesday, March 31 11pm - Wednesday, April 1 ??:??'
        ),
        (   # Single day event with None start time
            date(2015, 3, 31), None, date(2015, 3, 31), time(19, 30),
            'Tuesday, March 31 ??:??-7:30pm'
        ),
        (   # Single day event with None end time
            date(2015, 3, 31), time(15, 0), date(2015, 3, 31), None,
            'Tuesday, March 31 3pm-??:??'
        ),
    ]

    DATES = [
        (   # Some date
            date(2015, 3, 31), 'Tuesday, March 31'
        ),
        (   # Some other date
            date(2015, 4, 1), 'Wednesday, April 1'
        ),
        (   # Missing date
            None, '??? ??/??'
        )
    ]

    TIMES = [
        (   # Not sharing am/pm
            time(23), time(3, 30), '11pm-3:30am'
        ),
        (   # Sharing am/pm
            time(21), time(22), '9-10pm'
        ),
        (   # Missing start time
            None, time(3, 30), '??:??-3:30am'
        ),
        (   # Missing end time
            time(23), None, '11pm-??:??'
        ),
        (   # Mssing both start and end times
            None, None, '??:??-??:??'
        )
    ]

    def test_human_readable_datetime(self):
        """Test that :func:`~app.models.Event.human_readable_datetime` properly
        formats event dates and times into human readable date/time strings.
        """
        from eventum.models import Event
        for (start_date,
                start_time,
                end_date,
                end_time,
                string) in self.DATETIMES:
            event = Event(start_date=start_date,
                          start_time=start_time,
                          end_date=end_date,
                          end_time=end_time,
                          **self.EVENT_KWARGS)
            msg = self.ERROR_MSG.format('human readable datetime',
                                        string,
                                        event.human_readable_datetime())
            self.assertEqual(event.human_readable_datetime(), string, msg=msg)

    def test_human_readable_date(self):
        """Test that :func:`~app.models.Event.human_readable_date` properly
        formats event dates into human readable date strings.
        """
        from eventum.models import Event
        for event_date, string in self.DATES:
            event = Event(start_date=event_date,
                          start_time=None,
                          end_date=event_date,
                          end_time=None,
                          **self.EVENT_KWARGS)
            msg = self.ERROR_MSG.format('human readable date',
                                        string,
                                        event.human_readable_date())
            self.assertEqual(event.human_readable_date(), string, msg=msg)

    def test_human_readable_time(self):
        """Test that :func:`~app.models.Event.human_readable_time` properly
        formats event times into human readable time strings.
        """
        from eventum.models import Event
        any_date = date(2015, 3, 31)
        for start_time, end_time, string in self.TIMES:
            event = Event(start_date=any_date,
                          start_time=start_time,
                          end_date=any_date,
                          end_time=end_time,
                          **self.EVENT_KWARGS)
            msg = self.ERROR_MSG.format('human readable time',
                                        string,
                                        event.human_readable_time())
            self.assertEqual(event.human_readable_time(), string, msg=msg)

    def test_event_ending_on_midnight(self):
        """Test that events ending on midnight are properly formatted."""
        from eventum.models import Event
        start_date, start_time = date(2015, 3, 31), time(22)
        end_date, end_time = date(2015, 4, 1), time(0)

        event = Event(start_date=start_date,
                      start_time=start_time,
                      end_date=end_date,
                      end_time=end_time,
                      **self.EVENT_KWARGS)

        self.assertFalse(event.is_multiday())
        self.assertEqual(event.human_readable_date(), 'Tuesday, March 31')
        self.assertEqual(event.human_readable_time(), '10pm-12am')

    def test_event_starting_on_midnight(self):
        """Test that events starting on midnight are properly formatted."""
        from eventum.models import Event
        start_date, start_time = date(2015, 4, 1), time(00)
        end_date, end_time = date(2015, 4, 1), time(5, 30)

        event = Event(start_date=start_date,
                      start_time=start_time,
                      end_date=end_date,
                      end_time=end_time,
                      **self.EVENT_KWARGS)

        self.assertFalse(event.is_multiday())
        self.assertEqual(event.human_readable_date(), 'Wednesday, April 1')
        self.assertEqual(event.human_readable_time(), '12-5:30am')
