# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from webapp.models import Image


class Base(models.Model):
    pub_date = models.DateTimeField(
        "publicatie datum",
        blank=True,
        null=True
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

    class Meta:
        abstract = True


class Event(Base):
    """
    An Event can have multiple Edition objects.
    """
    name = models.CharField("Naam", max_length=200, unique=True)
    city = models.CharField("Plaats", max_length=200)
    slug = models.SlugField(unique=True)
    text = models.TextField("Tekst", blank=True, help_text="Korte omschrijving van dit evenement. Wat maakt dit evenement anders dan andere evenementen?")
    website = models.URLField(
        blank=True,
        help_text=u"Alleen de base url.",
    )
    image = models.ForeignKey(Image, verbose_name='event_image', blank=True, null=True)

    def __unicode__(self):
        return u"%s - %s" % (self.name, self.city)

    class Meta:
        verbose_name = u"evenement"
        verbose_name_plural = u"   Evenementen"

    def get_absolute_url(self):
        return reverse('race:event_detail', args=(self.slug, ))

    def get_edit_url(self):
        return reverse('race:event_update', args=(self.slug, ))

    def get_admin_url(self):
        return reverse('admin:race_event_change', args=(self.id,))


class Distance(Base):
    """
    Distance is a property of `Race`.
    """
    name = models.CharField(max_length=200, unique=True)
    order = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"Afstand"
        verbose_name_plural = u"Afstanden"
        ordering = ["order", ]


class Result(Base):
    """
    Result

    If no time is given, than that user still has to
    participate aka who-what-where.
    """
    user = models.ForeignKey(User, verbose_name="deelnemer")
    event = models.ForeignKey(Event)
    date = models.DateField()
    distance = models.ForeignKey(Distance)
    time = models.TimeField("Tijd", blank=True, null=True, help_text="HH:MM:SS")
    remarks = models.CharField(
        "Opmerkingen",
        max_length=200,
        blank=True,
        help_text=u"Podiumplaatsen zijn het vermelden waard. Bijvoorbeeld: '1e H50'.",
        )

    def __unicode__(self):
        return "%s %s %s %s %s" % (self.user, self.date, self.event, self.distance, self.time)

    class Meta:
        unique_together = (("user", "event", "date", "distance"),)
        verbose_name = "Wie wat waar / Uitslag"
        verbose_name_plural = "Wie wat waars / Uitslagen"
        ordering = ['-date', 'event', 'distance', 'time']
