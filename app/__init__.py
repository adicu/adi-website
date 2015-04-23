"""
.. module:: __init__
    :synopsis: This is where all our global variables and instantiation
        happens. If there is simple app setup to do, it can be done here, but
        more complex work should be farmed off elsewhere, in order to keep
        this file readable.

.. moduleauthor:: Dan Schlosser <dan@danrs.ch>
"""

import json
import logging

from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.assets import Environment, Bundle

from config import adi_config

db = MongoEngine()
app = None
adi = dict()
assets = None
gcal_client = None


def create_app(**config_overrides):
    """This is normal setup code for a Flask app, but we give the option
    to provide override configurations so that in testing, a different
    database can be used.
    """
    # we want to modify the global app, not a local copy
    global app
    global adi
    global assets
    global gcal_client
    app = Flask(__name__)

    # Load config then apply overrides
    app.config.update(config_overrides)

    from config import flask_config
    app.config.update(**flask_config.config)
    app.config.update(config_overrides)

    # load ADI specific configurations (ignore built-in methods)
    for attr in (x for x in dir(adi_config) if x[:2] != "__"):
        adi[attr] = getattr(adi_config, attr)

    # Initialize assets
    assets = Environment(app)
    register_scss()

    # Setup the database.
    db.init_app(app)

    # Initialize the Google Calendar API Client, but only if the api
    # credentials have been generated first.
    try:
        from app.lib.google_calendar import GoogleCalendarAPIClient
        gcal_client = GoogleCalendarAPIClient()
    except IOError:
        gae_environ = 'TRUE' if app.config['GOOGLE_AUTH_ENABLED'] else 'FALSE'
        raise Exception('Failed to find the Google Calendar credentials file '
                        'at `{}`, please create it by running:\n\n'
                        '    $ python manage.py --authorize\n'
                        'The environment variable GOOGLE_AUTH_ENABLED is '
                        'currently set to `{}`.  If set to FALSE, Google '
                        'Calendar calls will fail silently.'.format(
                            app.config['INSTALLED_APP_CREDENTIALS_PATH'],
                            gae_environ))
        exit(1)

    register_delete_rules()
    register_blueprints()

    from app.routes.base import register_error_handlers
    register_error_handlers(app)
    register_logger()
    return app


def register_logger():
    """Create an error logger and attach it to ``app``."""

    max_bytes = int(app.config["LOG_FILE_MAX_SIZE"]) * 1024 * 1024   # MB to B
    # Use "# noqa" to silence flake8 warnings for creating a variable that is
    # uppercase.  (Here, we make a class, so uppercase is correct.)
    Handler = logging.handlers.RotatingFileHandler  # noqa
    f_str = ('%(levelname)s @ %(asctime)s @ %(filename)s '
             '%(funcName)s %(lineno)d: %(message)s')

    access_handler = Handler(app.config["WERKZEUG_LOG_NAME"],
                             maxBytes=max_bytes)
    access_handler.setLevel(logging.INFO)
    logging.getLogger("werkzeug").addHandler(access_handler)

    app_handler = Handler(app.config["APP_LOG_NAME"], maxBytes=max_bytes)
    formatter = logging.Formatter(f_str)
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(formatter)

    app.logger.addHandler(app_handler)


def register_blueprints():
    """Registers all the Blueprints (modules) in a function, to avoid
    circular dependancies.

    Be careful rearranging the order of the app.register_blueprint()
    calls, as it can also result in circular dependancies.
    """
    from app.routes.admin import (admin, auth, events, media, posts,
                                  users, whitelist, api)
    admin_blueprints = [admin, auth, events, media, posts, users,
                        whitelist, api]

    for bp in admin_blueprints:
        app.register_blueprint(bp, url_prefix="/admin")

    from app.routes import blog, client
    blueprints = [blog, client]

    for bp in blueprints:
        app.register_blueprint(bp)


def register_delete_rules():
    """Registers rules for how Mongoengine handles the deletion of objects
    that are being referenced by other objects.

    See the documentation for :func:`mongoengine.model.register_delete_rule`
    for more information.

    All delete rules for User fields must by DENY, because User objects should
    never be deleted.  Lists of reference fields should PULL, to remove deleted
    objects from the list, and all others should NULLIFY
    """
    from app.models import Event, EventSeries, User, Post, BlogPost, Image
    from mongoengine import NULLIFY, PULL, DENY

    Event.register_delete_rule(EventSeries, 'events', PULL)
    Image.register_delete_rule(BlogPost, 'images', PULL)
    Image.register_delete_rule(User, 'image', NULLIFY)
    Image.register_delete_rule(BlogPost, 'featured_image', NULLIFY)
    Image.register_delete_rule(Event, 'image', NULLIFY)
    EventSeries.register_delete_rule(Event, 'parent_series', NULLIFY)
    User.register_delete_rule(Event, 'creator', DENY)
    User.register_delete_rule(Image, 'creator', DENY)
    User.register_delete_rule(Post, 'author', DENY)
    User.register_delete_rule(Post, 'posted_by', DENY)


def register_scss():
    """Registers the Flask-Assets rules for scss compilation.  This reads from
    ``config/scss.json`` to make these rules.
    """
    assets.url = app.static_url_path
    with open('config/scss.json') as f:
        bundle_instructions = json.loads(f.read())
        for _, bundle_set in bundle_instructions.iteritems():
            output_folder = bundle_set['output_folder']
            depends = bundle_set['depends']
            for bundle_name, instructions in bundle_set['rules'].iteritems():
                bundle = Bundle(*instructions['inputs'],
                                output=output_folder + instructions['output'],
                                depends=depends,
                                filters='scss')
                assets.register(bundle_name, bundle)


def run():
    """Runs the app."""
    app.run(host=app.config.get('HOST'), port=app.config.get('PORT'))
