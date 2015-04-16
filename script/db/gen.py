"""
.. module:: events
    :synopsis: This module runs scripts that load the database with test
        configurations. To run the scripts, run ``python manage.py db`` from
        the root directory.

.. moduleauthor:: Dan Schlosser <dan@schlosser.io>
"""

from mongoengine import connect
from mongoengine.queryset import DoesNotExist
from sys import argv, exit
from app.models import User, Event, EventSeries, Image, BlogPost
from script.cli import CLIColor, ProgressPrinter
from config.flask_config import MONGODB_SETTINGS
from images import create_images
from events import create_events
from posts import create_posts

argv0 = argv[0]

COMMAND_IMAGES = 'images'
COMMAND_EVENTS = 'events'
COMMAND_POSTS = 'posts'
COMMAND_ALL = 'all'
COMMANDS = set((COMMAND_IMAGES, COMMAND_EVENTS, COMMAND_POSTS, COMMAND_ALL))

WIPE_FLAGS = set(('--wipe', '-w'))
FORCE_FLAGS = set(('--force', '-f'))
QUIET_FLAGS = set(('--quiet', '-q'))
ALL_FLAGS = WIPE_FLAGS | FORCE_FLAGS | QUIET_FLAGS

USAGE = """Usage:

    python {exe} images|events|posts|all <options>

        Populates the database with test data. This can be run with:
            images: Downloads several dummy images and adds them to Eventum.
            events: Creates several events, with images if any exist.
            posts: Creates several blog posts, with images if any exist.
            all: All of the above.

        Available options:
            --quiet  (-q): Runs with minimal output
            --wipe   (-w): Wipes related databases.  If omitted, records that
                           already exist will not be updated.
            --force  (-f): Doesn't ask before wiping database.  Only relevant
                           if the --wipe option is used.
"""


def print_usage():
    """Prints a message describing this script's usage, and exits."""
    print USAGE.format(exe=argv0)
    exit(1)


class TestDataGenerator(object):
    """Loads the database with test data."""

    def __init__(self, command, flags):
        """Initializes the TestDataGenerator

        :param str command: One of the four following commands::

            COMMAND_IMAGES: Create new :class:`~app.models.Image` objects.
            COMMAND_EVENTS: Create new :class:`~app.models.Event` and
                            :class:`~app.models.EventSeries` objects.
             COMMAND_POSTS: Create new :class:`~app.models.BlogPost` objects.
               COMMAND_ALL: Do all of the above.

        :param flags: Flags passed to the function.  We assume all are valid.
        :type flags: set(str)
        """
        self.should_gen_images = command in (COMMAND_IMAGES, COMMAND_ALL)
        self.should_gen_events = command in (COMMAND_EVENTS, COMMAND_ALL)
        self.should_gen_posts = command in (COMMAND_POSTS, COMMAND_ALL)
        self.force = FORCE_FLAGS & flags
        self.wipe = WIPE_FLAGS & flags
        self.quiet = QUIET_FLAGS & flags

    def warn(self, db_name):
        """Print out a warning that we are about to wipe ``db_name``.  Prompts
        the user to confirm this deletion.

        If the ``--force`` flag is used, this check is skipped.

        :param str db_name: The name of the database to delete.
        """
        if not self.force:
            print CLIColor.underline(
                CLIColor.fail('WARNING!!! You are about wipe the '
                              '{} database!'.format(db_name)))
            cont = ''
            while cont == '':
                cont = raw_input('Do you want to continue? (yes/no): ')
            if cont[0] not in ('y', 'Y'):  # if the answer doesn't start with y
                print ('Exiting...')
                exit(1)

    def run(self):
        """Run the generation.  Uses the configurations passed to
        func:`__init__`.
        """

        # Setup: db connection, superuser, and printer.
        connect(MONGODB_SETTINGS['DB'])
        try:
            superuser = User.objects().get(gplus_id='super')
        except DoesNotExist:
            print ('Failed to get superuser.  Try running:\n'
                   '\texport GOOGLE_AUTH_ENABLED=TRUE')
        printer = ProgressPrinter(self.quiet)

        # Images
        if self.should_gen_images:
            if self.wipe:
                self.warn('Image')
                print CLIColor.warning('Wiping Image database.')
                Image.drop_collection()
            create_images(12, superuser, printer)

        # Blog posts
        if self.should_gen_posts:
            if self.wipe:
                self.warn('BlogPost')
                print CLIColor.warning('Wiping BlogPost database.')
                BlogPost.drop_collection()
            create_posts(10, superuser, printer)

        # Events and event series
        if self.should_gen_events:
            if self.wipe:
                self.warn('Event and EventSeries')
                print CLIColor.warning('Wiping Event database.')
                Event.drop_collection()
                print CLIColor.warning('Wiping EventSeries database.')
                EventSeries.drop_collection()
            create_events(superuser, printer)


def main(args):
    """Script runner.  Takes in the arguments to the function.  This might just
    be ``argv`` from :module:`sys`, or it might be a slightly modified version
    of ``argv``.

    :param args: The CLI arguments passed to the script.
    :type args: list(str)
    """

    # Update argv0 in case we're not being called from here.
    global argv0
    argv0 = args[0]

    if len(args) < 2:
        print CLIColor.fail('Command missing.')
        print_usage()

    # Parse command, which should be one of COMMANDS
    command = args[1]
    if command not in COMMANDS:
        print CLIColor.fail('Invalid command: ' + command)
        print_usage()

    # Parse flags, making a set 'options' containing all valid options
    flags = set(args[2:])

    if flags - ALL_FLAGS:  # There are invalid flags in 'flags'
        print CLIColor.fail('Invalid flags: ' + ' '.join(flags - ALL_FLAGS))
        print_usage()

    generator = TestDataGenerator(command, flags)
    generator.run()


if __name__ == '__main__':
    main(argv)
