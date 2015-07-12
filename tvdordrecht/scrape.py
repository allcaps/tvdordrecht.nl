import glob
import datetime
import os

from PIL import Image as PilImage
from bs4 import BeautifulSoup

from django.utils.text import slugify
from django.core.files import File
from django.conf import settings

from webapp.models import News, Image


def clean_up(soup):
    """
    Cleans the soup from unwanted tags and attributes.

    :param soup: BeautifulSoup
    :return: BeautifulSoup
    """

    for tag in soup.find_all(class_='page_info_bar'):
        tag.decompose()

    for tag in soup.find_all(class_='block_title'):
        tag.decompose()

    attributes = [
        'style',
        'onclick',
        'id',
        'font',
        'class',
        'language',
        'align',
        'id',
        'lang'
    ]
    tags = [
        'script',
    ]

    for attr in attributes:
        for tag in soup.find_all(attrs={attr:True}):
            del tag[attr]

    for tag in tags:
        for tg in soup.find_all(tag):
            tg.decompose()

    # TODO: Remove wrapping divs
    # TODO: fix br br to </p><p>

    return soup

def load_news():
    """
    Iterates over a folder and reads html from the files. Writes the relevant
    tags to News objects.

    :return:
    """

    for obj in News.objects.all():
        obj.delete()

    for filename in glob.glob('/Users/coen/Desktop/tvdordrecht_full_dl/www.tvdordrecht.nl/index.php*.html'):
        if 'print' not in filename:
            data = open(filename, 'r')
            soup = BeautifulSoup(data, 'html.parser')
            text = soup.find(id='content')
            if text:
                title = text.find(class_='block_title')
                if title:
                    title = ' '.join(title.stripped_strings)
                slug = slugify(title)[:50]

                date_tag = soup.find('span', attrs={'class':"info_bar_date"})
                if date_tag:
                    day, month, year = date_tag.string.split('-')
                    pub_date = datetime.datetime(int(year), int(month), int(day), 12, 0)

                    text = clean_up(text)

                    print('\n\n\n')
                    print(title)
                    print(slug)
                    print(text)
                    print(pub_date)

                    n = 2
                    original_slug = slug
                    while News.objects.filter(slug=slug).count():
                        slug = "%s-%d" %(original_slug, n)
                        n += 1

                    news = News(
                        title=title,
                        slug=slug,
                        text=text,
                        pub_date=pub_date,
                    )
                    news.save()
                    print ('\nsaved: ' + news.title)

def load_images():
    """
    Iterates over paths and writes all matching images to Django Image objects.

    :return: None
    """
    for obj in Image.objects.all():
        obj.delete()

    paths = [
        '/Users/coen/Desktop/tvdordrecht_full_dl/www.tvdordrecht.nl/userfiles/nieuwsarchief/*.*',
        '/Users/coen/Desktop/tvdordrecht_full_dl/www.tvdordrecht.nl/userfiles/clubnieuws/*.*',
    ]

    for path in paths:
        for filename in glob.glob(path):

            print(filename)

            data = open(filename, 'r')
            try:
                im = PilImage.open(data)
            except IOError:
                im = None

            if im and (im.size[0] > 60 or im.size[1] > 60):
                obj = Image()
                filename = os.path.basename(filename)
                obj.image.save(filename, File(data), save=True)

def clean_news():
    """
    Loops over all News objects and cleans the image path.
    Scales the first image up and sets it as a lead image on the news object.

    :return: None
    """
    for news in News.objects.all():
        soup = BeautifulSoup(news.text, 'html.parser')

        for n, tag in enumerate(soup.find_all('img')):
            filename = os.path.basename(tag['src'])
            tag['src'] = "/media/images/2015/06/30/" + filename
            tag['class'] = "img-responsive"

            if n == 0:
                obj = Image.objects.filter(image__contains=filename).first()
                if obj:
                    path = settings.MEDIA_ROOT + '/' + obj.image.name
                    im = PilImage.open(path)
                    new_size = tuple([x * 4 for x in im.size])
                    new_im = im.resize(new_size, PilImage.NEAREST)
                    new_im.save('tmp.jpg', format='JPEG', quality=80)
                    data = open('tmp.jpg', 'r')
                    new_obj = Image()
                    filename = slugify(news.title) + '.jpg'
                    new_obj.image.save(filename, File(data), save=True)
                    news.image = new_obj

        news.text = unicode(soup)
        news.save()

    # TODO: delete the temp file