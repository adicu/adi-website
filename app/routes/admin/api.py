"""
.. module:: api
    :synopsis: All routes on the ``api`` Blueprint.

.. moduleauthor:: Jett Andersen <jettca1@gmail.com>
"""

from datetime import datetime, timedelta, date

from flask import Blueprint, request, render_template, g, redirect, \
    url_for, flash, jsonify

from bson.objectid import ObjectId
from mongoengine.errors import DoesNotExist, ValidationError

from bson import json_util
import json

from app.models import Event, Image
from app.forms import CreateEventForm, EditEventForm, DeleteEventForm, UploadImageForm
from app.lib.decorators import login_required, requires_privilege

from app.lib.error import GoogleCalendarAPIError
from app.lib.events import EventsHelper
api = Blueprint('api', __name__)

@api.route('/api/events/this_week', methods=['GET'])
def events_this_week():
    """
    Get a json object containing information about all the events for the
    current week (Sunday to Sunday).
    
    **Route:** ``/admin/api/events/this_week

    **Methods:** ``GET`` 
    """

    today = date.today()
    last_sunday = datetime.combine(today - timedelta(days=(today.isoweekday() % 7)),
                                   datetime.min.time())
    next_sunday = last_sunday + timedelta(days=7)
    events = Event.objects(start_date__gte=last_sunday,
                              start_date__lt=next_sunday).order_by('start_date')
    event_dicts = [ event.to_jsonifiable() for event in events ]

    return json.dumps(event_dicts, default = json_util.default)
