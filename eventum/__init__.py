import logging
from eventum.lib.google_calendar import GoogleCalendarAPIClient
from eventum.config import eventum_config
from flask.ext.mongoengine import MongoEngine


class Eventum(object):
    EXTENSION_NAME = 'eventum'

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # Register ourselves as a Flask extension.
        app.extensions = getattr(app, 'extensions', {})
        if self.EXTENSION_NAME not in app.extensions:
            # This allows us to access the Eventum() instance from current_app.
            app.extensions[self.EXTENSION_NAME] = self

        self.app = app

        # Eventum Settings
        self._normalize_client_settings()
        self._setdefault_eventum_settings()

        # Mongoengine, and associated delete rules.
        self.register_delete_rules()
        self.db = MongoEngine(app)

        # Blueprints
        self.register_blueprints()

        # TODO: SCSS for Eventum

        # Google Calendar API Client
        self.gcal_client = GoogleCalendarAPIClient()

        # Error handlers, before_request, after_request, context_processor, etc
        from eventum.routes.base import register_error_handlers
        register_error_handlers(app)

        # Logging
        self.register_logger()

    def _normalize_client_settings(self):
        if 'EVENTUM_SETTINGS' in self.app.config:
            # Eventum settings provided as a dictionary.
            for key, value in self.app.config['EVENTUM_SETTINGS'].iteritems():
                self.app.config['EVENTUM_' + key] = value

    def _setdefault_eventum_settings(self):
        for attr in (a for a in dir(eventum_config) if a[:2] != "__"):
            self.app.config.setdefault(attr, getattr(eventum_config, attr))

    def register_blueprints(self):
        from eventum.routes.admin import (admin, auth, events, media, posts,
                                          users, whitelist, api)
        admin_blueprints = [admin, auth, events, media, posts, users,
                            whitelist, api]

        for bp in admin_blueprints:
            self.app.register_blueprint(
                bp,
                url_prefix=self.app.config['EVENTUM_URL_PREFIX'])

    def register_delete_rules(self):
        """Registers rules for how Mongoengine handles the deletion of objects
        that are being referenced by other objects.

        See the documentation for
        :func:`mongoengine.model.register_delete_rule` for more information.

        All delete rules for User fields must by DENY, because User objects
        should never be deleted.  Lists of reference fields should PULL, to
        remove deleted objects from the list, and all others should NULLIFY
        """
        from eventum.models import (Event, EventSeries, User, Post, BlogPost,
                                    Image)
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

    def register_logger(self):
        """Create an error logger and attach it to ``app``."""

        # Convert MB -> B
        max_bytes = (
            int(self.app.config['EVENTUM_LOG_FILE_MAX_SIZE']) * 1024 * 1024)

        # Use '# noqa' to silence flake8 warnings for creating a variable that
        # is uppercase.  (Here, we make a class, so uppercase is correct.)
        Handler = logging.handlers.RotatingFileHandler  # noqa
        f_str = ('%(levelname)s @ %(asctime)s @ %(filename)s '
                 '%(funcName)s %(lineno)d: %(message)s')

        access_handler = Handler(self.app.config['EVENTUM_WERKZEUG_LOG_NAME'],
                                 maxBytes=max_bytes)
        access_handler.setLevel(logging.INFO)
        logging.getLogger('werkzeug').addHandler(access_handler)

        app_handler = Handler(self.app.config['EVENTUM_APP_LOG_NAME'],
                              maxBytes=max_bytes)
        formatter = logging.Formatter(f_str)
        app_handler.setLevel(logging.INFO)
        app_handler.setFormatter(formatter)
        self.app.logger.addHandler(app_handler)
