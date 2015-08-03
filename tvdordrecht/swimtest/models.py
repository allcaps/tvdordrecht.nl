from datetime import datetime, timedelta
combine = datetime.combine

from django.db import models
from django.template.defaultfilters import date as _date
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

date = datetime(2000, 1, 1).date()


class SwimTest(models.Model):
    date = models.DateField()

    def get_absolute_url(self):
        return reverse('swim-test', args=(self.pk, ))

    def __unicode__(self):
        return _date(self.date, 'l j F Y')

    class Meta:
        verbose_name = u"zwemtest"
        verbose_name_plural = u"zwemtesten"
        ordering = ['-date',]


class Record(models.Model):
    swim_test = models.ForeignKey(SwimTest)
    user = models.ForeignKey(
        User,
        verbose_name="Atleet",
        )
    time_100 = models.TimeField(u'100 m')
    time_200 = models.TimeField(u'200 m')
    time_300 = models.TimeField(u'300 m')
    time_400 = models.TimeField(u'400 m')
    time_500 = models.TimeField(u'500 m')
    split_100 = models.TimeField(u'100 split', blank=True, null=True)
    split_200 = models.TimeField(u'200 split', blank=True, null=True)
    split_300 = models.TimeField(u'300 split', blank=True, null=True)
    split_400 = models.TimeField(u'400 split', blank=True, null=True)
    split_500 = models.TimeField(u'500 split', blank=True, null=True)
    pace_time = models.TimeField(
        u'Pacetime',
        blank=True,
    )
    remarks = models.CharField(
        'Opmerkingen',
        max_length=200,
        blank=True,
    )

    def display_pace_time(self):
        return str(self.pace_time)

    display_pace_time.short_description = 'Pace time'
    display_pace_time.admin_order_field = 'pace_time'

    def date_property(self):
        return self.swim_test.date

    date = property(date_property)

    def save(self, *args, **kwargs):
        # Calculate the pace time. (500m time - 100m time) / 4
        # To calculate time you need a datetime object `dt`.
        date = datetime(2000, 1, 1).date()
        pt = (combine(date, self.time_500) - combine(date, self.time_100)) / 4
        # Round to seconds.
        if pt.microseconds >= 500000:
            pt += timedelta(seconds=1)
        pt -= timedelta(microseconds=pt.microseconds)
        # Set pace time.
        self.pace_time = str(pt)
        # Set `split_100` is the same as `time_100`.
        self.split_100 = self.time_100
        # Others splits are current time - prev time.
        split = (combine(date, self.time_200) - combine(date, self.time_100))
        self.split_200 = str(split)
        split = (combine(date, self.time_300) - combine(date, self.time_200))
        self.split_300 = str(split)
        split = (combine(date, self.time_400) - combine(date, self.time_300))
        self.split_400 = str(split)
        split = (combine(date, self.time_500) - combine(date, self.time_400))
        self.split_500 = str(split)
        super(Record, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = u"Testresultaat"
        verbose_name_plural = u"Testresultaten"
        unique_together = (('swim_test', 'user'),)
        ordering = ['pace_time',]

def get_swimtest_url(self):
    return reverse('swimtest-user', args=(self.id,))

User.add_to_class('get_swimtest_url', get_swimtest_url)
