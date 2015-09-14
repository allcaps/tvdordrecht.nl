from django.test import TestCase

from .utils import (
    table_of_contents,
)


class UtilsMethodTests(TestCase):

    def test_table_of_contents_empty(self):
        """ Empty text returns empty stings. """
        toc, html = table_of_contents(u"")
        self.assertEqual(toc, u"")
        self.assertEqual(html, u"")

    def test_table_of_contents_single(self):
        """ Single heading returns one toc item. """
        toc, html = table_of_contents(u"<h2>Heading</h2>")
        self.assertEqual(toc, u'<li class="toc_h2"><a href="#heading">Heading</a></li>')
        self.assertEqual(html, u'<h2 id="heading"><a href="#heading" title="Permanente link naar Heading">Heading</a></h2>')

    def test_table_of_contents_respect_stings_before_and_afther(self):
        """ Single heading, string before and after. """
        toc, html = table_of_contents(u"String before<h2>Heading</h2>String after")
        self.assertEqual(toc, u'<li class="toc_h2"><a href="#heading">Heading</a></li>')
        self.assertEqual(html, u'String before<h2 id="heading"><a href="#heading" title="Permanente link naar Heading">Heading</a></h2>String after')

    def test_table_of_contents_respect_tags_before_and_after(self):
        """ Single heading, paragraph before and after. """
        toc, html = table_of_contents(u'<p class="lead">String before</p><h2>Heading</h2><p>String after</p>')
        self.assertEqual(toc, u'<li class="toc_h2"><a href="#heading">Heading</a></li>')
        self.assertEqual(html, u'<p class="lead">String before</p><h2 id="heading"><a href="#heading" title="Permanente link naar Heading">Heading</a></h2><p>String after</p>')

    def test_table_of_contents_triple(self):
        """ Triple heading, test for unique ids. """
        toc, html = table_of_contents(u"<h2>Heading</h2><h2>Heading</h2><h2>Heading</h2>")
        self.assertEqual(
            toc,
            u"".join(
                [
                    u'<li class="toc_h2"><a href="#heading">Heading</a></li>',
                    u'<li class="toc_h2"><a href="#heading-1">Heading</a></li>',
                    u'<li class="toc_h2"><a href="#heading-2">Heading</a></li>'
                ]
            )
        )
        self.assertEqual(
            html,
            u"".join(
                [
                    u'<h2 id="heading"><a href="#heading" title="Permanente link naar Heading">Heading</a></h2>',
                    u'<h2 id="heading-1"><a href="#heading-1" title="Permanente link naar Heading">Heading</a></h2>',
                    u'<h2 id="heading-2"><a href="#heading-2" title="Permanente link naar Heading">Heading</a></h2>'
                ]
            )
        )

    def test_table_of_contents_strip_non_breaking_space(self):
        """ Single heading, strip `&nbsp;`. """
        toc, html = table_of_contents(u'<h2>Dead&nbsp;Parrot</h2>')
        self.assertEqual(toc, u'<li class="toc_h2"><a href="#dead-parrot">Dead Parrot</a></li>')
        self.assertEqual(html, u'<h2 id="dead-parrot"><a href="#dead-parrot" title="Permanente link naar Dead Parrot">Dead Parrot</a></h2>')

    # def test_table_of_contents_remove_inner_tags(self):
    # def test_table_of_contents_remove_inner_tags_with_non_breaking_space(self):