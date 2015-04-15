import sys
sys.path.append('..')

import urllib
from mongoengine import connect
from mongoengine.queryset import DoesNotExist
from sys import argv
from os.path import exists

from app.models import Image, User
from config.flask_config import MONGODB_SETTINGS, UPLOAD_FOLDER
from app.lib.cli import CLIColor


def gen_test_data(wipe=False, force=False, update=False, verbose=True):
    connect(MONGODB_SETTINGS['DB'])
    try:
        superuser = User.objects().get(gplus_id='super')
    except DoesNotExist:
        print ("Failed to get superuser.  Try running:\n"
               "\texport GOOGLE_AUTH_ENABLED=TRUE")

    if wipe:
        if not force:
            print (CLIColor.underline(
                CLIColor.fail("WARNING!!! You are about to wipe the DB!")))
            cont = ""
            while cont == "":
                cont = raw_input("Do you want to continue? (yes/no): ")
            if cont[0] not in ('y', 'Y'):
                print ("Exiting...")
                exit(1)

        print "wiping..."
        # Event.drop_collection()

    populate_images(superuser)


BASE_URL = "http://lorempixel.com/{}/{}/"
BASE_FILENAME = "test_photo_{}x{}.jpeg"


def populate_images(superuser, force=False):
    test_images = download_images(force)
    for filename, path in test_images:
        image = Image(filename=filename,
                      default_path=path,
                      creator=superuser)
        image.save()


def download_images(force=False):
    print "Downloading images..."
    print "-" * 40
    images = []
    failures = []
    skips = []
    for width in range(400, 1600, 100):
        height = width / 2
        filename = BASE_FILENAME.format(width, height)
        path = UPLOAD_FOLDER + filename
        url = BASE_URL.format(width, height)

        print filename + (" " * (32 - len(filename))),
        if force or not exists(path):
            try:
                urllib.urlretrieve(url, path)
                images.append((filename, path))
                print "Success"

            except IOError:
                failures.append((filename, ''))
                print " Failed"
        else:
            skips.append((filename, path))
            print "   Skip"
    print "-" * 40
    print "Done. {} successful, {} skipped, {} failed.".format(len(images),
                                                               len(skips),
                                                               len(failures))
    return images + skips

if __name__ == '__main__':
    options = set(argv)
    update = bool(set(('-u', '--update')) & options)
    wipe = bool(set(('-w', '--wipe')) & options)
    force = bool(set(('-f', '--force')) & options)
    verbose = not bool(set(('-q', '--quiet')) & options)
    gen_test_data(wipe, force, update, verbose)
