import urllib
from os.path import exists

from app.models import Image
from config.flask_config import UPLOAD_FOLDER

BASE_URL = "http://lorempixel.com/{}/{}/"
BASE_FILENAME = "test_photo_{}x{}.jpeg"


def create_images(num_images, superuser, printer, force=False):
    print "Generating images..."
    printer.line()
    successes = []
    failures = []
    skips = []
    for width in range(400, 1600, (1600 - 400) / num_images):
        height = width / 2
        filename = BASE_FILENAME.format(width, height)
        path = UPLOAD_FOLDER + filename
        url = BASE_URL.format(width, height)

        printer.begin_status_line(filename)
        if force or not exists(path):
            try:
                urllib.urlretrieve(url, path)
            except IOError:
                failures.append((filename, ''))
                printer.status_fail()
                continue  # Failed to download, move on to the next image.

        if Image.objects(filename=filename).count() == 0:
            image = Image(filename=filename,
                          default_path=path,
                          creator=superuser)
            image.save()
            successes.append((filename, path))
            printer.status_success()
        else:
            skips.append((filename, path))
            printer.status_skip()

    printer.line()
    printer.results(successes, skips, failures)
    return successes + skips
