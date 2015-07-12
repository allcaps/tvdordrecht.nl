# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from model_utils.models import TimeStampedModel


class Category(TimeStampedModel):
    title = models.CharField("titel", max_length=200)
    slug = models.SlugField(unique=True)
    text = models.TextField("Omschrijving", blank=True)
    #sortorder = models.IntegerField("sortering")

    class Meta:
        verbose_name = "categorie"
        verbose_name_plural = "categorieën"
        ordering = ('title', )

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/activity/%s/' % self.slug

    def get_admin_url(self):
        return "/admin/activity/category/%s/" % self.id


class Activity(TimeStampedModel):
    publish = models.BooleanField("publiceren", default=True)
    category = models.ForeignKey(
        Category, 
        verbose_name="categorie",
        related_name="activity_category",
        )
    title = models.CharField("Wat", max_length=200)
    slug = models.SlugField()
    start_date = models.DateField("Begindatum")
    start_time = models.TimeField("Begintijd", blank=True, null=True)
    end_date = models.DateField("Einddatum", blank=True, null=True)
    end_time = models.TimeField("Eindtijd", blank=True, null=True)
    all_day = models.BooleanField(
        "All-day",
        default=False,
        help_text=u"Als aangevinkt gelden alleen de datum-velden, tijd-velden vervallen.",
        )
    description = models.TextField("Opmerkingen", blank=True)
    participants = models.ManyToManyField(
        User,
        verbose_name="deelnemers",
        blank=True,
        related_name="activity_participants",
        )

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "activiteit"
        verbose_name_plural = "activiteiten"
        ordering = ('-start_date', '-start_time')
        unique_together = (('start_date', 'category', 'slug'),)

    # def get_absolute_url(self):
    #     return "/activiteiten/%s/%s/%s/" \
    #         % (self.start_date.strftime("%Y/%m/%d"),
    #            self.category.slug,
    #            self.slug)

    def get_absolute_url(self):
        return "/activiteiten/%s/" % self.id

    def get_admin_url(self):
        return "/admin/webapp/activity/%s/" % self.id

    def save(self, *args, **kwargs):
        if self.all_day:
            self.start_time = None
            self.end_time = None
            if self.start_date == self.end_date:
                self.end_date = None
        super(Activity, self).save(*args, **kwargs)
