#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from django.template.defaultfilters import date
from django.core.urlresolvers import reverse

from model_utils.models import TimeStampedModel


class Discipline(TimeStampedModel):
    title = models.CharField("titel", max_length=200)
    slug = models.SlugField(unique=True)
    text = models.TextField("Omschrijving", blank=True)

    class Meta:
        verbose_name = "discipline"
        verbose_name_plural = "disciplines"

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('training:discipline_list')

    def get_admin_url(self):
        return reverse('admin:training_discipline_change', args=(self.pk,))


class Location(TimeStampedModel):
    title = models.CharField("titel", max_length=200)
    address = models.CharField("adres", max_length=200)
    city = models.CharField("plaats", max_length=200)
    slug = models.SlugField(unique=True)
    text = models.TextField("Omschrijving", blank=True)

    class Meta:
        verbose_name = "locatie"
        verbose_name_plural = "locaties"

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('training:location_list')

    def get_admin_url(self):
        return reverse('admin:training_location_change', args=(self.pk,))


class Session(TimeStampedModel):
    start = models.DateTimeField("Start", unique=True)
    discipline = models.ForeignKey(
        Discipline,
        verbose_name="discipline",
        related_name="session_training",
        )
    location = models.ForeignKey(
        Location, 
        verbose_name="locatie",
        related_name="session_location",
        blank=True,
        null=True,
        )
    trainer = models.ForeignKey(
        User, 
        verbose_name="trainer",
        related_name="session_trainer",
        blank=True,
        null=True,
        )
    message = models.CharField(
        "Notificatie",
        max_length=400,
        blank=True,
        help_text="Voor uitzonderingen ten opzichte van normaal. " +
        "Bijvoorbeeld: 'Flippers menemen'."
        )
    cancel = models.BooleanField(
        u"Afgelast",
        default=False,
        help_text=u"Vink aan als de training afgelast is. " +
            u"Als afgelast, dan is een notificatie verplicht.",
        )
    participants = models.ManyToManyField(
        User,
        blank=True,
        related_name="session_participants",
        )

    def __unicode__(self):
        date_time = date(self.start, "l j F Y")
        return "%s %s" % (
            date_time,
            self.discipline.title,
        )

    class Meta:
        verbose_name = "trainingssessie"
        verbose_name_plural = "trainingssessies"
        ordering = ('start',)
        unique_together = (('start', 'discipline', 'location'),)

    def get_absolute_url(self):
        return reverse(
            'training:session',
            kwargs={
                'year': self.start.year,
                'month': self.start.month,
                'day': self.start.day,
                'pk': self.pk,
            }
        )

    def get_admin_url(self):
        return reverse('admin:training_session_change', args=(self.pk,))
