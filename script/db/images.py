import urllib
from os.path import exists

from app.models import Image
from config.flask_config import UPLOAD_FOLDER
from app.lib.cli import CLIColor

BASE_URL = "http://lorempixel.com/{}/{}/"
BASE_FILENAME = "test_photo_{}x{}.jpeg"
WIDTH = 40


def create_images(num_images, superuser, force=False):
    print "Downloading images..."
    print "-" * WIDTH
    successes = []
    failures = []
    skips = []
    for width in range(400, 1600, (1600 - 400) / num_images):
        height = width / 2
        filename = BASE_FILENAME.format(width, height)
        path = UPLOAD_FOLDER + filename
        url = BASE_URL.format(width, height)

        print filename + (" " * (WIDTH - 8 - len(filename))),
        if force or not exists(path):
            try:
                urllib.urlretrieve(url, path)
            except IOError:
                failures.append((filename, ''))
                print " Failed"
                continue  # Failed to download, move on to the next image.

        if Image.objects(filename=filename).count() == 0:
            successes.append((filename, path))
            image = Image(filename=filename,
                          default_path=path,
                          creator=superuser)
            image.save()
            print "Success"
        else:
            skips.append((filename, path))
            print "   Skip"

    print "-" * WIDTH
    print "Done. ",

    if successes:
        print CLIColor.ok_green("{} successful,".format(len(successes))),
    else:
        print "0 successful,",

    print "{} skipped,".format(len(skips)),

    if failures:
        print CLIColor.ok_green("{} failed.".format(len(failures))),
    else:
        print "0 failed."

    return successes + skips
