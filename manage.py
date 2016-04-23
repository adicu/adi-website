"""
.. module:: manage
    :synopsis: This script facilitates test database entry generation and
        migration tools. run ``python manage.py -h`` for more.

.. moduleauthor:: Dan Schlosser <dan@schlosser.io>
"""

from argparse import ArgumentParser

from eventum.script.migrate import backfill_blog, import_images
from eventum.script.db.gen import TestDataGenerator, ACTIONS, FLAGS

COMMAND_MIGRATE = 'migrate'
MIGRATE_DESCRIPTION = """
Migrates data from Jekyll to Eventum.  Imports data from data/old-website-data,
which is a submodule.
"""
MIGRATE_HELP = """
blog: Backfills blog posts from data/old-website-data/posts.\n
images: Imports images from data/old-website-data/images.
"""
MIGRATE_IMAGES = 'images'
MIGRATE_BLOG = 'blog'
MIGRATE_OPTIONS = (MIGRATE_IMAGES, MIGRATE_BLOG)

COMMAND_DB = 'db'
DB_DESCRIPTION = """
Populates Mongo with test images, blog posts, events, and / or event series.
"""
DB_HELP = """
Which database to populate with test data.  Selecting "all" will populate all
three.
"""

COMMAND_HELP = """
Either migrate old data to Eventum, or populate the database.
"""


def parse_args():
    """Constructs an argument parser, with two subcommands: "migrate" and
    "db".  Run ``python manage.py -h" to see more. Then give the parsed
    arguments.

    :returns: The arguments, parsed.
    :rtype: :class:`argparse.Namespace`
    """
    parser = ArgumentParser(description='Manage Eventum.')
    subparsers = parser.add_subparsers(dest='command', help=COMMAND_HELP)
    db_parser = subparsers.add_parser(COMMAND_DB,
                                      description=DB_DESCRIPTION)
    db_parser.add_argument('action',
                           choices=ACTIONS,
                           help=DB_HELP)
    for flags, help in FLAGS:
        db_parser.add_argument(*flags,
                               action='store_true',
                               help=help)
    migrate_parser = subparsers.add_parser(COMMAND_MIGRATE,
                                           description=MIGRATE_DESCRIPTION)
    migrate_parser.add_argument('action',
                                choices=MIGRATE_OPTIONS,
                                help=MIGRATE_HELP)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    if args.command == COMMAND_MIGRATE:
        if args.action == MIGRATE_IMAGES:
            import_images.import_from_directory('data/old-website-data/images')
        elif args.action == MIGRATE_BLOG:
            backfill_blog.backfill_from_jekyll('data/old-website-data/posts')
    elif args.command == COMMAND_DB:
        generator = TestDataGenerator(args.action,
                                      quiet=args.quiet,
                                      wipe=args.wipe,
                                      force=args.force)
        generator.run()
