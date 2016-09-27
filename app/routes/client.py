"""
.. module:: client
    :synopsis: All routes on the ``client`` Blueprint.

.. moduleauthor:: Dan Schlosser <dan@danrs.ch>
"""

import json
from flask import (Blueprint, render_template, abort, redirect, url_for,
                   request, current_app)
from eventum.models import Event, BlogPost
from datetime import datetime, date, timedelta
from mongoengine import Q

client = Blueprint('client', __name__)

_resources = None
_labs_data = None
_companies = None

now = datetime.now()

ONE_TRIPLE = 3  # One set of three small events
ONE_LARGE_AND_TRIPLE = 4  # One large event and one set of three small events
NUM_PAST_EVENTS_FOR_FRONTPAGE = 6  # Two triples
NUM_EVENTS_PER_PAGE = 10


@client.route('/', methods=['GET'])
def index():
    """View the ADI homepage.

    **Route:** ``/``

    **Methods:** ``GET``
    """
    # cast date.today() to a datetime
    today = datetime.combine(date.today(), datetime.min.time())

    # Ending on a future date, or today at a future time. The events should be
    # published, and should be chronological.
    # We limit to four events, one large event and one set of three events.
    events = (Event.objects(Q(end_date__gte=today))
                   .filter(published=True)
                   .order_by('start_date', 'start_time')
                   .limit(ONE_LARGE_AND_TRIPLE))

    # sort published posts chronologically back in time
    all_blog_posts = (BlogPost.objects(published=True)
                              .order_by('-date_published'))
    latest_blog_post = all_blog_posts[0] if all_blog_posts else None

    return render_template('index.html',
                           events=events,
                           blog_post=latest_blog_post)


@client.route('/events/devfest', methods=['GET'])
@client.route('/devfest', methods=['GET'])
def devfest():
    """View the DevFest landing page.

    **Route:** ``/devfest``, ``/events/devfest``

    **Methods:** ``GET``
    """
    return redirect("http://devfe.st")


@client.route('/contact', methods=['GET'])
def contact():
    """View contact information.

    **Route:** ``/contact``

    **Methods:** ``GET``
    """
    return render_template('contact.html')


@client.route('/feedback', methods=['GET'])
def feedback():
    """Submit feedback on past ADI events.

    **Route:** ``/feedback``

    **Methods:** ``GET``
    """
    return render_template('feedback.html')


@client.route('/foundry', methods=['GET'])
def foundry():
    '''View information about ADI foundry
    **Route:** ``/foundry``

    **Methods:** ``GET``
    '''

    return render_template('foundry.html')


@client.route('/mentorship', methods=['GET'])
def mentorship():
    '''View information about mentorship program
    **Route:** ``/mentorship``

    **Methods:** ``GET``
    '''

    return render_template('mentorship.html')


@client.route('/jobfair', methods=['GET'])
def jobfair():
    """View the ADI Startup Career Fair page.

    **Route:** ``/jobfair``

    **Methods:** ``GET``
    """
    force = request.args.get('force') is not None
    companies = _get_companies(force=force)
    return render_template('jobfair.html', companies=companies)


def _get_companies(force=False):
    global _companies
    if not _companies or force:
        with open(current_app.config['COMPANIES_PATH']) as f:
            _companies = json.loads(f.read()).get('2016')
    return _companies


@client.route('/labs', methods=['GET'])
def labs():
    """View information about ADI Labs

    **Route:** ``/labs``

    **Methods:** ``GET``
    """
    force = request.args.get('force') is not None
    labs_data = _get_labs_data(force=force)
    return render_template('labs.html', data=labs_data)


def _get_labs_data(force=False):
    global _labs_data
    if not _labs_data or force:
        with open(current_app.config['LABS_DATA_PATH']) as f:
            _labs_data = json.loads(f.read())
    return _labs_data


@client.route('/learn', methods=['GET'])
def learn():
    """Alias for :func:`resources`.

    **Route:** ``/learn``

    **Methods:** ``GET``
    """
    return redirect(url_for('.resources'))


@client.route('/resources', methods=['GET'])
def resources():
    """Learn to code! View resources for learning how to program different
    websites.

    **Route:** ``/resources``

    **Methods:** ``GET``
    """
    force = request.args.get('force') is not None
    resources_data = _get_resources(force=force)
    return render_template('resources.html', resources=resources_data)


def _get_resources(force=False):
    global _resources
    if not _resources or force:
        with open(current_app.config['RESOURCES_PATH']) as f:
            _resources = json.loads(f.read())
    return _resources


@client.route('/events', methods=['GET'])
def events():
    """View the latest events.

    **Route:** ``/events``

    **Methods:** ``GET``
    """
    today = date.today()
    weekday = (today.isoweekday() % 7) + 1  # Sun: 1, Mon: 2, ... , Sat: 7
    last_sunday = datetime.combine(today - timedelta(days=weekday + 7),
                                   datetime.min.time())
    next_sunday = datetime.combine(today + timedelta(days=7 - weekday),
                                   datetime.min.time())
    recent_and_upcoming = Event.objects(published=True).order_by('start_date',
                                                                 'start_time')

    # Sort recent events chronologically backwards in time
    recent_events = (recent_and_upcoming.filter(end_date__lt=today)
                                        .order_by('-start_date')
                                        .limit(NUM_PAST_EVENTS_FOR_FRONTPAGE))

    events_this_week = list(
        recent_and_upcoming.filter(end_date__gte=today,
                                   start_date__lt=next_sunday)
    )

    # One large event, and one set of three small events
    upcoming_events = (recent_and_upcoming.filter(start_date__gt=next_sunday)
                                          .limit(ONE_LARGE_AND_TRIPLE))

    more_past_events = bool(Event.objects(published=True,
                                          start_date__lte=last_sunday).count())

    return render_template('events/events.html',
                           recent_events=recent_events,
                           events_this_week=events_this_week,
                           upcoming_events=upcoming_events,
                           more_past_events=more_past_events)


@client.route('/events/<int:index>', methods=['GET'])
def event_archive(index):
    """View old events.

    **Route:** ``/events/<index>``

    **Methods:** ``GET``

    :param int index: The page to fetch
    """
    if index <= 0:
        return redirect(url_for('.events'))

    # Get all events that occur on this page or on subsequent pages, and order
    # them chronologically back in time
    today = date.today()
    events = (Event.objects(published=True, end_date__lt=today)
                   .order_by('-start_date')
                   .skip(NUM_PAST_EVENTS_FOR_FRONTPAGE +
                         (index - 1) * NUM_EVENTS_PER_PAGE))

    # If there are no such events, redirect to the pevious page
    if not events:
        return redirect(url_for('.event_archive', index=index - 1))

    # There is always a previous page, but there is only a next page if there
    # are more events after this page
    previous_index = index - 1
    next_index = index + 1 if len(events) > NUM_EVENTS_PER_PAGE else None

    # Use .limit() to only show NUM_EVENTS_PER_PAGE events per page
    return render_template('events/archive.html',
                           events=events.limit(NUM_EVENTS_PER_PAGE),
                           previous_index=previous_index,
                           next_index=next_index)


@client.route('/events/<slug>', methods=['GET'])
def event(slug):
    """View a specific non-recurring event, or the next upcoming instance of
    a recurring event.

    **Route:** ``/events/<slug>``

    **Methods:** ``GET``

    :param str slug: The unique slug ID for the post.
    """
    if Event.objects(published=True, slug=slug).count() == 0:
        abort(404)  # Either invalid event ID or duplicate IDs.

    event = Event.objects(published=True, slug=slug)[0]

    if event.is_recurring:
        upcoming_event_instances = (Event.objects(published=True,
                                                  start_date__gte=date.today(),
                                                  slug=slug)
                                         .order_by('start_date'))
        if upcoming_event_instances:
            event = upcoming_event_instances[0]
        else:
            event = event.parent_series.events[-1]

    return render_template('events/event.html',
                           event=event,
                           now=now,
                           upcoming_events=_upcoming_events_triple(event))


@client.route('/events/<slug>/<int:index>', methods=['GET'])
def recurring_event(slug, index):
    """View a specific instance of a recurring event.

    **Route:** ``/events/<slug>/<index>``

    **Methods:** ``GET``

    :param str slug: The unique slug ID for the post.
    :param int index: The instance of the event to fetch.
    """
    if Event.objects(published=True, slug=slug).count() == 0:
        abort(404)  # Either invalid event ID or duplicate IDs.

    event = Event.objects(published=True, slug=slug)[0]

    if not event.is_recurring or not event.parent_series:
        return redirect(url_for('.event', slug=slug))

    if len(event.parent_series.events) <= index:
        abort(404)

    event = event.parent_series.events[index]
    return render_template('events/event.html',
                           event=event,
                           now=now,
                           upcoming_events=_upcoming_events_triple(event))


def _upcoming_events_triple(event):
    """Returns a set of three upcoming events, excluding ``event``.

    :param event: The event to exclude
    :type event: :class:`~app.models.Event`
    :returns: The set of three events
    :rtype: Mongoengine.queryset
    """
    return (Event.objects(published=True,
                          start_date__gte=date.today(),
                          id__ne=event.id)
                 .order_by('start_date')
                 .limit(ONE_TRIPLE))


@client.route('/jade', methods=['GET'])
def jade():
    return render_template('jade.html')


# @client.route('/join', methods=['GET'])
# def gbody():
#     return render_template('join.html')
