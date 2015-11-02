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
from eventum import Eventum

from config import adi_config


app = None
adi = dict()
eventum = None


def create_app(**config_overrides):
    """This is normal setup code for a Flask app, but we give the option
    to provide override configurations so that in testing, a different
    database can be used.
    """
    # we want to modify the global app, not a local copy
    global app
    global adi
    global eventum

    app = Flask(__name__)

    # Load config then apply overrides
    from config import flask_config
    app.config.update(**flask_config.config)
    app.config.update(config_overrides)

    # Eventum
    eventum = Eventum(app)

    # load ADI specific configurations (ignore built-in methods)
    for attr in (x for x in dir(adi_config) if x[:2] != "__"):
        adi[attr] = getattr(adi_config, attr)

    # Initialize assets
    assets = Environment(app)
    register_scss(assets)

    # Blueprints
    register_blueprints()

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
