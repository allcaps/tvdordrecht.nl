#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import os
import re
from PIL import Image as PILImage
from bs4 import BeautifulSoup

from django.template.defaultfilters import slugify
from django.conf import settings
from django.utils.html import strip_tags


# def make_default_size(self, width=276, height=276):
#     filename = os.path.join(settings.MEDIA_ROOT, self.image.name)
#     try:
#         image = PILImage.open(filename)
#         if width < image.size[0] or height < image.size[1]:
#             image.convert('RGB')
#             image.thumbnail([width, height], PILImage.ANTIALIAS)
#             if image.format == "jpg" or "JPG" or "jpeg" or "JPEG":
#                 image.save(filename, image.format, quality=75)
#             else:
#                 image.save(filename, image.format)
#     except:
#         pass


def edit_image(self):
    path = self.image.path
    basedir = os.path.dirname(path)
    base, ext = os.path.splitext(os.path.basename(path))
    for thumb in glob.glob(r"%s/%s_[c|t]_*x*%s" % (basedir, base, ext)):
        os.remove(thumb)
    # Edit original
    im = PILImage.open(path)
    if self.image_editing == "90":
        im = im.transpose(PILImage.ROTATE_270)
    if self.image_editing == "180":
        im = im.transpose(PILImage.ROTATE_180)
    if self.image_editing == "270":
        im = im.transpose(PILImage.ROTATE_90)
    if self.image_editing == "double":
        new_size = tuple([x * 2 for x in im.size])
        im = im.resize(new_size, PILImage.NEAREST)
    im.save(path)
    return


def clean_tables(html):
    soup = BeautifulSoup(html)
    [tag.replaceWith(tag.contents[0]) for tag in soup.select('th > p')]
    [tag.replaceWith(tag.contents[0]) for tag in soup.select('th > strong')]
    [tag.replaceWith(tag.contents[0]) for tag in soup.select('td > p')]
    [tag.replaceWith(tag.contents[0]) for tag in soup.select('td > strong')]
    for table in soup.select('table'):
        # Add bootstrap class to each table.
        table['class'] = 'table table-striped table-condensed'
        # The first row is a header
        # Change td in th.
        for td in table.find('tr').find_all('td'):
            td.name = 'th'
        # The first row is a header and should be wrapped in 'thead'.
        for tr in table.find('tr'):
            if not tr.parent.parent.name == "thead":
                row = tr.parent.extract()
                thead = soup.new_tag("thead")
                thead.insert(0, row)
                table.insert(0, thead)
    return unicode(soup)


def make_table(html, absolute_url=""):
    """
    Generates table of contents and HTML width an unique id for every heading
    """
    table_of_contents = u""
    soup = BeautifulSoup(html)
    ids = []

    for tag in soup.find_all('h2'): #re.compile('^h')

        # Clean the title before constructing an id.
        # Remove all breaks.
        [br.extract() for br in tag.findAll('br')]
        if tag.contents and tag.contents[0]:
            # Removes non breaking space from title.
            title = tag.contents[0].replace('&nbsp;', ' ')
        else:
            title = ""

        id = slugify(title)

        # Make sure the id is unique
        counter = 1
        temp_id = id
        while id in ids:
            id = '%s_%d' % (temp_id, counter)
            counter += 1
        ids.append(id)

        # Replace heading element a new one.
        tag['id'] = id
        temp = BeautifulSoup(
            u'<%s id="%s"><a href="#%s" title="Permanente link naar %s">%s</a></%s>' %
            (tag.name, id, id, title, title, tag.name)
        )
        tag.replaceWith(temp)

        # Add an link to the table of contents.
        table_of_contents += u'<li class="toc_%s"><a href="%s#%s">%s</a></li>' % \
                             (tag.name, absolute_url, id, title)

    html = unicode(soup)
    return table_of_contents, html


def get_description(html):
    """
    Contents for Meta tag description.
    Aka the description text for Search Result Pages.
    """
    text = strip_tags(html)
    if isinstance(text, str):
        return " ".join(text.split())[:250]
    else:
        return ""

import string
from random import choice


def rot(n, text):
    from string import ascii_lowercase as lc, ascii_uppercase as uc
    lookup = string.maketrans(lc + uc, lc[n:] + lc[:n] + uc[n:] + uc[:n])
    return ''.join([c.translate(lookup) for c in str(text)])


def obfuscate_email(html):
    """
    Email obfuscate in a attempt to block email harvesters. At least the ones
    that don't evaluate JS. Note that the wisest thing to not receive SPAM is
    to NOT publish your email address at all.
    Although we have SPAM filters in place, we don't want to feed the troll.
    """
    soup = BeautifulSoup(html)
    # Strip out all mailto links and replace them with the email in plain text.
    [tag.replaceWith(tag['href'].replace("mailto:", "")) for tag in soup.select('a[href^=mailto]')]
    # Find and replace all emails with a JS constructing the email.
    html = unicode(soup)
    emails = re.findall(r'[\w.-]+@[\w.-]+', html)
    for index, email in enumerate(emails):
        tag = """'<a href="mailto:%s">%s</a>'""" % (email, email)
        encode_number = choice(range(2, 24))
        encoded = rot(encode_number, tag)
        decode_number = 26 - encode_number

        js = """
        <script id="script-%d">
            $(function() {
                function rot(s, i) {
                    return s.replace(/[a-zA-Z]/g, function (c) {
                        return String.fromCharCode((c <= 'Z' ? 90 : 122) >= (c = c.charCodeAt(0) + i) ? c : c - 26);
                    });
                }
                $('#script-%s').after(rot(%s, %d));
            });
        </script>
        """ % (index, index, encoded, decode_number)
        html = html.replace(email, js, 1)
    print html
    return html
