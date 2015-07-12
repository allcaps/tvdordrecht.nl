# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.template import defaultfilters
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from webapp.models import Image

"""
An `Event` can have multiple Editions.
An `Edition` can have multiple Races.
A `Race` can have multiple Results.
A `Result` belongs to one User.

A result with time == Null is a who what where. Aka an indication the user will
participate.
"""


class Event(models.Model):
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
    # Meta fields
    pub_date = models.DateTimeField("publicatie datum", blank=True, null=True)
    owner = models.ForeignKey(User, verbose_name="Eigenaar", blank=True, null=True, editable=False, related_name="%(class)s_owner")
    last_modified_by = models.ForeignKey(User, verbose_name="Laatst bewerkt door", blank=True, null=True, editable=False, related_name="%(class)s_last_modified_by")
    last_modified = models.DateTimeField("laatst bewerkt", blank=True, null=True, editable=False, auto_now=True)

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


class Edition(models.Model):
    """
    An Edition can have multiple Race objects.
    """
    event = models.ForeignKey(Event)
    date = models.DateField()

    def __unicode__(self):
        return defaultfilters.date(self.date, "j F Y")

    class Meta:
        unique_together = (("event", "date"),)
        verbose_name = u"editie"
        verbose_name_plural = u"  Edities"
        ordering = ["-date", ]

    def get_absolute_url(self):
        return reverse('race:event_detail', kwargs={'slug': self.event.slug, })

    def get_edit_url(self):
        return reverse(
            'race:edition_update',
            kwargs={
                'event_slug': self.event.slug,
                'pk': self.pk,
            }
        )


class Distance(models.Model):
    """
    Distance is a property of `Race`.
    """
    name = models.CharField(max_length=200, unique=True)
    order = models.CharField(max_length=200, blank=True)
    default = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"Afstand"
        verbose_name_plural = u"Afstanden"
        ordering = ["default", "order", ]


class Race(models.Model):
    """
    A Race can have multiple Results
    """
    edition = models.ForeignKey(Edition)
    distance = models.ForeignKey(Distance)

    def __unicode__(self):
        return self.distance.name

    def get_absolute_url(self):
        return reverse('race:event_detail', args=(self.edition.event.slug,))

    def get_edit_url(self):
        return reverse(
            'race:event_update',
            kargs={
                'event_slug': self.edition__event.slug,
                'pk': self.pk,
            }
        )

    class Meta:
        unique_together = (("edition", "distance"),)
        verbose_name = "wedstrijd"
        verbose_name_plural = " Wedstrijden"
        ordering = ['distance']


class Result(models.Model):
    """
    Result

    If no time is given, than this is a indication that the user will
    participate aka who-what-where.
    """
    user = models.ForeignKey(User, verbose_name="deelnemer")
    race = models.ForeignKey(Race, verbose_name="Wedstrijd")
    time = models.TimeField("Tijd", blank=True, null=True, help_text="HH:MM:SS")
    remarks = models.CharField(
        "Opmerkingen",
        max_length=200,
        blank=True,
        help_text=u"Podiumplaatsen zijn het vermelden waard. Bijvoorbeeld: '1e H50'.",
        )

    def __unicode__(self):
        time = self.time or "(Geen)"
        return "%s %s" % (self.user, time)

    def event_name(self):
        return self.race.edition.event

    def edition(self):
        return self.race.edition

    def choice_label(self):
        return "%s %s %s" % (self.edition(), self.event_name(), self.race.distance)

    class Meta:
        unique_together = (("user", "race"),)
        verbose_name = "uitslag"
        verbose_name_plural = "uitslagen"
        ordering = ['race__edition', 'time']
