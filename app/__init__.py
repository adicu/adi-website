"""
.. module:: __init__
    :synopsis: This is where all our global variables and instantiation
        happens. If there is simple app setup to do, it can be done here, but
        more complex work should be farmed off elsewhere, in order to keep
        this file readable.

.. moduleauthor:: Dan Schlosser <dan@danrs.ch>
"""

import json
from flask import Flask
from flask.ext.assets import Environment, Bundle
from webassets.filter import get_filter
from eventum import Eventum


app = None
eventum = None


def create_app(**config_overrides):
    """This is normal setup code for a Flask app, but we give the option
    to provide override configurations so that in testing, a different
    database can be used.
    """
    # we want to modify the global app, not a local copy
    global app
    global eventum

    app = Flask(__name__)

    # Load config then apply overrides
    app.config.from_object('config.flask_config')
    app.config.update(config_overrides)

    # Initialize assets
    assets = Environment(app)
    register_scss(assets)

    print "="*10, app.config['DEBUG'], '='*10

    # Eventum
    eventum = Eventum(app)

    # # Augment Models
    # from app.models import augment_models
    # augment_models()

    # Blueprints
    register_blueprints()

    print "="*10, app.config['DEBUG'], '='*10

    return app


def register_blueprints():
    """Registers all the Blueprints (modules) in a function, to avoid
    circular dependancies.

    Be careful rearranging the order of the app.register_blueprint()
    calls, as it can also result in circular dependancies.
    """
    from app.routes import blog, client
    blueprints = [blog, client]

    for bp in blueprints:
        app.register_blueprint(bp)


def register_scss(assets):
    """Registers the Flask-Assets rules for scss compilation.  This reads from
    ``config/scss.json`` to make these rules.

    We expire files using filenames:
    http://webassets.readthedocs.org/en/latest/expiring.html#expire-using-the-filename
    """
    assets.append_path(app.static_folder, app.static_url_path)
    with open('config/scss.json') as f:
        bundle_instructions = json.loads(f.read())
        for _, bundle_set in bundle_instructions.iteritems():
            output_folder = bundle_set['output_folder']
            depends = bundle_set['depends']
            for bundle_name, instructions in bundle_set['rules'].iteritems():
                # Use filename expiration

                output_filename = (output_folder +
                                   instructions['output'].rstrip('.css') +
                                   '.%(version)s.css')
                bundle = Bundle(*instructions['inputs'],
                                output=output_filename,
                                depends=depends,
                                filters=('scss', 'cssmin'))
                assets.register(bundle_name, bundle)


def run():
    """Runs the app."""
    app.run(host=app.config.get('HOST'), port=app.config.get('PORT'))
