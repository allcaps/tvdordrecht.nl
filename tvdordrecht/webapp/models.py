# -*- coding: utf-8 -*-
import os
import glob
from datetime import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.template import Context

from utils import edit_image

keyword_help_text = """
    Alleen relevante keywords. Niet relevante keywords (die niet in de tekst 
    voorkomen) doen pagina's zakken.<br>
    Bij een leeg keywordveld worden keywords gegenereerd op basis van de 
    inhoud van het tekstveld.
    """

description_help_text = """
    Maximaal 250 karakters (Google zoekresultaten geven alleen de eerste 150 
    karakters weer).<br>
    Maak een relevante description. Bij voorkeur met tekst die op de pagina 
    voorkomt.</br>
    Bij een leeg descriptionveld wordt description gegenereerd op basis van de 
    inhoud van het tekstveld.
    """

sortorder_help_text = """
    Als er meerdere afbeeldingen in een foto-album staan, worden ze standaard 
    op alfabetische volgorde weergeven. Om de volgorde te wijzigen geef je een 
    sortering (getal) bij alle te ordenen afbeeldigen in.
    """

image_help_text = """
    Deze afbeelding komt op een vaste positie. Gebruik het afbeeldings-icoon
    in de text-editor om afbeeldingen tussen de lopende tekst in te voegen.
    """

EDIT_CHOICES = (
    (u'90', u'90°'),
    (u'180', u'180° '),
    (u'270', u'270°'),
    (u'double', u'Double the size')
)


class Image(models.Model):
    image = models.ImageField(
        "afbeelding", 
        upload_to='images/%Y/%m/%d', 
        height_field="height", 
        width_field="width",
    )
    caption = models.CharField(
        "bijschrift", 
        max_length=600, 
        blank=True,
    )
    sortorder = models.IntegerField(
        "Sortering", 
        blank=True, 
        null=True, 
        help_text=sortorder_help_text,
    )
    height = models.IntegerField(
        blank=True, 
        editable=False,
    )
    width = models.IntegerField(
        blank=True, 
        editable=False,
    )
    # Edit
    image_editing = models.CharField(
        "Afbeelding roteren", 
        choices=EDIT_CHOICES, 
        blank=True, 
        max_length=100, 
        default=""
    )
    # Meta fields
    pub_date = models.DateTimeField(
        "publicatie datum", 
        blank=True, 
        null=True,
    )
    owner = models.ForeignKey(
        User, 
        verbose_name="Eigenaar", 
        blank=True, 
        null=True, 
        editable=False, 
        related_name="%(class)s_owner",
    )
    last_modified_by = models.ForeignKey(
        User, 
        verbose_name="Laatst bewerkt door", 
        blank=True, 
        null=True, 
        editable=False, 
        related_name="%(class)s_last_modified_by",
    )
    last_modified = models.DateTimeField(
        "laatst bewerkt", 
        blank=True, 
        null=True, 
        editable=False, 
        auto_now=True,
    )

    class Meta:
        verbose_name = "Afbeelding"
        verbose_name_plural = "Afbeeldingen"
        ordering = ['-pub_date', ]

    def __unicode__(self):
        return self.image.name

    def filename(self):
        return self.image.name

    def get_absolute_url(self):
        return settings.MEDIA_URL + self.image.name

    def save(self, *args, **kwargs):
        super(Image, self).save()
        if self.image_editing:
            edit_image(self)
            self.image_editing = ""
        self.delete_thumbnails()
        get_template('images.html').render(Context({"image": self.image, }))
        # make_default_size(self, width=1024, height=1024)
        super(Image, self).save()

    def delete(self, using=None):
        self.delete_thumbnails()
        super(Image, self).delete()

    def delete_thumbnails(self):
        root = settings.MEDIA_ROOT
        file_name = self.image
        basedir = os.path.dirname("%s%s" % (root, file_name))
        base, ext = os.path.splitext(os.path.basename(str(file_name)))
        for obj in glob.glob(r"%s/%s_[c|t]_*x*%s" % (basedir, base, ext)):
            os.remove(obj)

    def list_thumbnail(self):
        img, ext = str(self.image).rsplit('.', 1)
        return """
            <a href="/admin/webapp/image/%s">
                <img src="/media/%s_t_132x132.%s?now=%s" alt="" />
            </a>
            """ % (self.id, img, ext, datetime.now().isoformat())

    list_thumbnail.short_description = 'thumbnail'
    list_thumbnail.allow_tags = True

    def inline_urls(self):
        """
        Display inline urls in list view
        """
        try:
            img, ext = self.image.name.rsplit('.', 1)
        except ValueError:
            img, ext = self.image.name, ""
        return """
            <p>
                <label for="inline_l_{uid}">Groot:</label>
                <input
                    id="inline_l_{uid}"
                    type="text"
                    value="/media/{img}_t_360x1200.{ext}"
                    readonly="readonly" />
            </p>
            <p>
                <label for="inline_s_{uid}">Klein:</label>
                <input
                    id="inline_s_{uid}"
                    type="text"
                    value="/media/{img}_t_132x132.{ext}"
                    readonly="readonly" />
            </p>
            """.format(
                uid=self.id,
                img=img,
                ext=ext
            )
    inline_urls.short_description = "Inline afbeelding-url's"
    inline_urls.allow_tags = True


class Menu(models.Model):
    title = models.CharField(
        "titel",
        max_length=200,
    )
    text = models.TextField(
        "tekst",
        blank=True,
    )
    image = models.ForeignKey(
        Image, 
        verbose_name="afbeelding",
        blank=True,
        null=True,
        related_name="%(class)s_image",
        help_text=image_help_text
    )
    html = models.TextField(
        "html",
        null=True,
        blank=True,
        editable=False,
    )
    table_of_contents = models.TextField(
        "table of contents", 
        null=True,
        blank=True,
        editable=False,
    )
    # Advanced
    slug = models.SlugField(unique=True)
    sortorder = models.IntegerField(
        "sortering", 
        blank=True, 
        null=True,
    )
    # Meta fields
    pub_date = models.DateTimeField(
        "publicatie datum", 
        blank=True, 
        null=True,
    )
    owner = models.ForeignKey(
        User, 
        verbose_name="Eigenaar", 
        blank=True, 
        null=True, 
        editable=False, 
        related_name="%(class)s_owner",
    )
    last_modified_by = models.ForeignKey(
        User, 
        verbose_name="Laatst bewerkt door", 
        blank=True, 
        null=True, 
        editable=False, 
        related_name="%(class)s_last_modified_by",
    )
    last_modified = models.DateTimeField(
        "laatst bewerkt", 
        blank=True, 
        null=True, 
        editable=False, 
        auto_now=True,
    )
    keywords = models.TextField(
        blank=True, 
        help_text=keyword_help_text,
    )
    description = models.TextField(
        blank=True, 
        max_length=250, 
        help_text=description_help_text,
    )

    class Meta:
        verbose_name = "menu-item"
        verbose_name_plural = "menu"
        ordering = ('sortorder', )

    def __unicode__(self):
        return self.title

    def get_admin_url(self):
        return reverse('admin:webapp_menu_change', args=(self.id,))

    def get_absolute_url(self):
        if self.slug == "home":
            return "/"
        else:
            return reverse('webapp:menu', args=(self.slug,))


class PageQuerySet(models.query.QuerySet):
    def live(self):
        return self.filter(publish=True)


class PageManager(models.Manager):
    """
    This manager makes it possible to loop over all life pages.
    As required by the main menu.
    {% for page in i.page.live %}
    """
    use_for_related_fields = True

    def get_queryset(self):
        return PageQuerySet(self.model)

    def live(self):
        return self.get_queryset().live()


class Page(models.Model):
    # , limit_choices_to=
    # {'id__in':[int(obj.id) for obj in Menu.objects.exclude(slug='home') \
    #   .exclude(slug='nieuws')] })
    menu = models.ForeignKey(
        Menu,
        related_name="page"
    )
    title = models.CharField(
        "titel",
        max_length=200
    )
    image = models.ForeignKey(
        Image,
        verbose_name="afbeelding",
        blank=True,
        null=True,
        related_name="%(class)s_image",
        help_text=image_help_text
    )
    text = models.TextField(
        "tekst",
        blank=True
    )
    html = models.TextField(
        "html",
        null=True,
        blank=True,
        editable=False
    )
    table_of_contents = models.TextField(
        "table of contents",
        null=True,
        blank=True,
        editable=False
    )
    # Advanced
    slug = models.SlugField(unique=True)
    publish = models.BooleanField(
        "publiceren",
        default=True
    )
    sortorder = models.IntegerField(
        "sortering",
        blank=True,
        null=True
    )
    # Meta fields
    pub_date = models.DateTimeField(
        "publicatie datum",
        blank=True,
        null=True,
        editable=False
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Eigenaar",
        blank=True,
        null=True,
        editable=False,
        related_name="%(class)s_owner"
    )
    last_modified_by = models.ForeignKey(
        User,
        verbose_name="Laatst bewerkt door",
        blank=True,
        null=True,
        editable=False,
        related_name="%(class)s_last_modified_by"
    )
    last_modified = models.DateTimeField(
        "laatst bewerkt",
        blank=True,
        null=True,
        editable=False,
        auto_now=True
    )
    keywords = models.TextField(
        blank=True,
        help_text=keyword_help_text
    )
    description = models.TextField(
        blank=True,
        max_length=250,
        help_text=description_help_text
    )

    objects = PageManager()

    class Meta:
        verbose_name = "pagina"
        verbose_name_plural = "pagina's"
        ordering = ('sortorder', 'title')
        unique_together = (("menu", "slug"),)

    def __unicode__(self):
        return self.title

    def get_admin_url(self):
        return reverse('admin:webapp_page_change', args=(self.id,))

    def get_absolute_url(self):
        return reverse('webapp:page_detail', args=(self.menu.slug, self.slug))


class News(models.Model):
    title = models.CharField(
        "titel",
        max_length=200
    )
    text = models.TextField("tekst")
    image = models.ForeignKey(
        Image,
        verbose_name="afbeelding",
        blank=True,
        null=True,
        related_name="%(class)s_image",
        help_text=image_help_text
    )
    # Advanced
    slug = models.SlugField(unique=True)
    publish = models.BooleanField(
        "publiceren",
        default=True
    )
    # Meta fields
    pub_date = models.DateTimeField(
        "publicatie datum",
        blank=True,
        null=True
    )
    owner = models.ForeignKey(
        User,
        verbose_name="gemaakt door",
        blank=True,
        null=True,
        related_name="%(class)s_owner"
    )
    last_modified_by = models.ForeignKey(
        User,
        verbose_name="Laatst bewerkt door",
        blank=True,
        null=True,
        editable=False,
        related_name="%(class)s_last_modified_by"
    )
    last_modified = models.DateTimeField(
        "laatst bewerkt",
        blank=True,
        null=True,
        editable=False,
        auto_now=True
    )
    keywords = models.TextField(
        blank=True,
        help_text=keyword_help_text
    )
    description = models.TextField(
        blank=True,
        max_length=250,
        help_text=description_help_text
    )
        
    class Meta:
        verbose_name = "nieuws-item"
        verbose_name_plural = "nieuws"
        ordering = ["-pub_date", ]

    def __unicode__(self):
        return self.title
       
    def get_admin_url(self):
        return reverse('admin:webapp_news_change', args=(self.id,))
        
    def get_absolute_url(self):
        return reverse(
            'webapp:news_detail',
            kwargs={
                'year': self.pub_date.year,
                'month': self.pub_date.month,
                'day': self.pub_date.day,
                'pk': self.pk,
                'slug': self.slug,
            }
        )

    def get_update_url(self):
        return reverse(
            'webapp:news_update',
            kwargs={
                'year': self.pub_date.year,
                'month': self.pub_date.month,
                'day': self.pub_date.day,
                'news_pk': self.pk,
                'slug': self.slug,
                'pk': self.image.pk,
            }
        )
