import random
from datetime import datetime, timedelta
from mongoengine.queryset import DoesNotExist, MultipleObjectsReturned
from app.models import Image, Event, EventSeries
from lorem import LOREM_EVENT, LOREM_SNIPPET, LOREM_ADJECTIVES

TIMEDELTAS = [timedelta(hours=4),   # upcoming
              timedelta(hours=4),   # same time
              timedelta(hours=-4),  # just happend
              ] + [timedelta(days=offset) for offset in range(-6, 6)]


def create_events(superuser, printer):
    print 'Generating events...'
    printer.line()
    generator = EventGenerator(superuser, printer)
    datetimes = (datetime.now() + d for d in TIMEDELTAS)
    successes, skips, failures = generator.create_events(datetimes)
    printer.line()
    printer.results(successes, skips, failures)
    made = successes + skips

    print 'Generating event series...'
    generator = EventGenerator(superuser, printer)
    printer.line()
    successes, skips, failures = generator.create_weekly_event()
    printer.line()
    printer.results(successes, skips, failures)
    made += successes + skips

    return made


class EventGenerator():

    def __init__(self, superuser, printer):
        self.superuser = superuser
        self.printer = printer
        self.is_recurring = False
        self.index = 0
        self.successes = []
        self.failures = []
        self.skips = []

    def next(self, slug=None, **kwargs):
        # Setup internals
        self.index += 1

        # Create and return the event
        slug = slug if slug else self._slug()
        self.printer.begin_status_line('<Event slug="{}">'.format(slug))
        try:
            event = Event.objects.get(slug=slug,
                                      start_date=self.start_datetime.date())
            self.skips.append(event)
            self.printer.status_skip()
        except DoesNotExist:
            event = self.make_event(slug=slug, **kwargs)
            event.save()
            self.successes.append(event)
            self.printer.status_success()
        except MultipleObjectsReturned:
            print slug
            raise
        return event

    def create_events(self, start_datetimes):
        for dt in start_datetimes:
            self.start_datetime = dt
            self.next()
        return self.successes, self.skips, self.failures

    def create_weekly_event(self, num_events=12):
        self.is_recurring = True
        slug = 'recurring'
        self.printer.begin_status_line('<EventSeries slug="{}">'.format(slug))
        try:
            series = EventSeries.objects.get(slug=slug)
            self.skips.append(series)
            self.printer.status_skip()
        except DoesNotExist:
            series = self.make_series(slug, num_events)
            series.save()
            self.successes.append(series)
            self.printer.status_success()

        date = datetime.now() - timedelta(days=num_events / 2 * 7)
        for i in range(num_events):
            # increment datetime
            self.start_datetime = date + timedelta(days=7 * i)
            # make the next event
            event = self.next(slug=slug, parent_series=series)
            event.save()
            # add the event to the series
            series.events.append(event)

        series.save()

        return self.successes, self.skips, self.failures

    def make_series(self, slug, num_events):
        return EventSeries(frequency="weekly",
                           every=1,
                           slug=slug,
                           ends_on=False,
                           ends_after=True,
                           num_occurrences=num_events,
                           recurrence_summary=self._recurrence_summary())

    def make_event(self, slug, **kwargs):
        return Event(title=self._title(),
                     creator=self.superuser,
                     location=self._location(),
                     slug=slug,
                     start_date=self._start_date(),
                     end_date=self._end_date(),
                     start_time=self._start_time(),
                     end_time=self._end_time(),
                     short_description_markdown=LOREM_SNIPPET,
                     long_description_markdown=LOREM_EVENT,
                     published=True,
                     date_published=self._date_published(),
                     is_recurring=self.is_recurring,
                     image=self._image(),
                     facebook_url=self._facebook_url(),
                     **kwargs)

    def _title(self):
        return '{} Test Event {}'.format(random.choice(LOREM_ADJECTIVES),
                                         self.index)

    def _slug(self):
        return 'test-event-{}'.format(self.index)

    def _location(self):
        return 'Some {} place'.format(
            random.choice(LOREM_ADJECTIVES).lower())

    def _start_date(self):
        return self.start_datetime.date()

    def _end_date(self):
        return self.start_datetime.date()

    def _start_time(self):
        return self.start_datetime.time()

    def _end_time(self):
        return (self.start_datetime + timedelta(hours=1)).time()

    def _date_published(self):
        return (datetime.combine(self._start_date(), self._start_time()) -
                timedelta(days=7))

    def _recurrence_summary(self):
        return 'Test recurrence'

    def _facebook_url(self):
        return 'https://www.facebook.com/ADICU#idx={}'.format(self.index)

    def _image(self):
        return random.choice(Image.objects())

    def _event_image(self):
        image = self._image()
        return image.filename if image else ''
