"""
.. module:: regex
    :synopsis: Regexes to be used around the app.

.. moduleauthor:: Dan Schlosser <dan@danrs.ch>
"""

from config.flask_config import config

SLUG_REGEX = r'[0-9a-zA-Z-]+'
FILENAME_REGEX = r'[\w\-@\|\(\)]+'
FULL_FILENAME_REGEX = "{fname}({ext})".format(
    fname=FILENAME_REGEX,
    ext="|".join(config['ALLOWED_UPLOAD_EXTENSIONS']))
EXTENSION_REGEX = "|".join(config['ALLOWED_UPLOAD_EXTENSIONS'])
