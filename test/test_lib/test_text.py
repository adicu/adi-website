"""
.. module:: test_text
    :synopsis: Tests for the :mod:`~app.lib.text` module.

.. moduleauthor:: Dan Schlosser <dan@danrs.ch>
"""
from test.base import TestingTemplate
from eventum.lib.text import clean_markdown


class TestTextHelpers(TestingTemplate):
    """Test the date, time, and datetime formatting in the Event model."""

    ERROR_MSG = 'Incorrect:\nexpected: "{}"\n     got: "{}"'

    MARKDOWN_EXPECTATIONS = [
        ('**Bold** text is unbolded.', 'Bold text is unbolded.'),
        ('So is *underlined* text.', 'So is underlined text.'),
        ('An [](http://empty-link).', 'An.'),
        ('A [test](https://adicu.com)', 'A test (https://adicu.com)'),
        ('A [test](http://adicu.com)', 'A test (http://adicu.com)'),
        ('A [test](garbage) passes.', 'A test passes.'),
        ('An ![image](http://anything) gets removed.', 'An gets removed.'),
        ('An ![image](garbage), [link](http://adicu.com), and an '
         '[![image in a link](imgurl)](http://adicu.com).',
         'An, link (http://adicu.com), and an.'),
    ]

    def test_clean_markdown(self):
        for md_in, md_out in self.MARKDOWN_EXPECTATIONS:
            output = clean_markdown(md_in)
            self.assertEqual(output,
                             md_out,
                             msg=self.ERROR_MSG.format(md_out, output))
