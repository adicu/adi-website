import random
from datetime import datetime, timedelta
from app.models import BlogPost, Image
from mongoengine.queryset import DoesNotExist
from lorem import LOREM_ADJECTIVES, LOREM_BLOG_POST

BACKUP_IMAGE_URL = 'http://lorempixel.com/800/450'


def create_posts(superuser, printer):
    print 'Generating blog posts...'
    generator = PostGenerator(superuser, printer)
    printer.line()
    datetimes = [datetime.now() + timedelta(days=-7 * i) for i in range(10)]
    successes, skips, failures = generator.create_posts(datetimes)
    printer.line()
    printer.results(successes, skips, failures)
    return successes + skips


class PostGenerator(object):

    def __init__(self, superuser, printer):
        self.superuser = superuser
        self.printer = printer
        self.index = 0
        self.successes = []
        self.failures = []
        self.skips = []
        self.images = None

    def create_posts(self, datetimes):
        for dt in datetimes:
            self.date_published = dt
            self.next()
        return self.successes, self.skips, self.failures

    def next(self):
        self.index += 1
        slug = self._slug()
        self.printer.begin_status_line('<BlogPost slug="{}">'.format(slug))
        try:
            blog_post = BlogPost.objects.get(slug=slug)
            self.skips.append(blog_post)
            self.printer.status_skip()
        except DoesNotExist:
            blog_post = self.make_post()
            blog_post.save()
            self.successes.append(blog_post)
            self.printer.status_success()

    def make_post(self):
        return BlogPost(title=self._title(),
                        author=self.superuser,
                        markdown_content=self._markdown_content(),
                        images=self._images(),
                        featured_image=self._featured_image(),
                        slug=self._slug(),
                        categories=self._categories(),
                        tags=self._tags(),
                        published=True,
                        date_published=self.date_published,
                        posted_by=self.superuser)

    def _title(self):
        return '{} Test Post {}'.format(random.choice(LOREM_ADJECTIVES),
                                        self.index)

    def _slug(self):
        return 'test-post-{}'.format(self.index)

    def _categories(self):
        return []

    def _tags(self):
        return []

    def _featured_image(self):
        return random.choice(self._images())

    def _images(self):
        # Fetch self.images if it hasn't been fetched
        if self.images is None:
            self.images = list(Image.objects().limit(5))
        return self.images

    def _markdown_content(self):
        # The blog post LOREM has two format string spots for images.
        # filenames = [image.filename for image in self._images()[:2]]
        filenames = [BACKUP_IMAGE_URL for i in range(2)]
        return LOREM_BLOG_POST.format(*filenames)
