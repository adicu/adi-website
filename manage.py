from sys import argv, exit

from script.migrate import backfill_blog, import_images
from script.db import gen

USAGE = """Usage:

    python {exe} migrate blog|images

        Migrates Jekyll data.  This can be run with:
        - blog: Backfills blog posts from data/old-website-data/posts.
        - images: Imports images from data/old-website-data/images.

    python {exe} db images|events|posts|all <options>

        Populates the database with test data. This can be run with:
        - images: Downloads several dummy images and adds them to Eventum.
        - events: Creates several events, with images if any exist.
        - posts: Creates several blog posts, with images if any exist.
        - all: All of the above.
"""


def print_usage():
    print USAGE.format(exe=argv[0])
    exit(1)


if __name__ == '__main__':

    if len(argv) < 2 or argv[1] not in ('migrate', 'db'):
        print_usage()

    if argv[1] == 'migrate':
        if len(argv) != 3 or argv[2] not in ('blog', 'images'):
            print_usage()

        if argv[2] == 'blog':
            backfill_blog.backfill_from_jekyll('data/old-website-data/posts')
        if argv[2] == 'images':
            import_images.import_from_directory('data/old-website-data/images')

    if argv[1] == 'db':
        # Call gen.main with ["<argv0> db", "<argv2>", "<argv3>", ...]
        gen.main([argv[0] + ' db'] + argv[2:])
