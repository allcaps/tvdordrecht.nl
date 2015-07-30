# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('race', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='edition',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='edition',
            name='event',
        ),
        migrations.AlterUniqueTogether(
            name='race',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='race',
            name='distance',
        ),
        migrations.RemoveField(
            model_name='race',
            name='edition',
        ),
        migrations.AlterModelOptions(
            name='result',
            options={'ordering': ['date', 'event', 'distance', 'time'], 'verbose_name': 'wie wat waar / uitslag', 'verbose_name_plural': 'wie wat waars / uitslagen'},
        ),
        migrations.AddField(
            model_name='result',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 7, 29, 17, 6, 12, 676118, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result',
            name='distance',
            field=models.ForeignKey(default=1, to='race.Distance'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result',
            name='event',
            field=models.ForeignKey(default=1, to='race.Event'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, verbose_name=b'laatst bewerkt', null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='last_modified_by',
            field=models.ForeignKey(related_name='result_last_modified_by', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'Laatst bewerkt door'),
        ),
        migrations.AddField(
            model_name='result',
            name='owner',
            field=models.ForeignKey(related_name='result_owner', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'Eigenaar'),
        ),
        migrations.AddField(
            model_name='result',
            name='pub_date',
            field=models.DateTimeField(null=True, verbose_name=b'publicatie datum', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='result',
            unique_together=set([('user', 'event', 'date', 'distance')]),
        ),
        migrations.DeleteModel(
            name='Edition',
        ),
        migrations.RemoveField(
            model_name='result',
            name='race',
        ),
        migrations.DeleteModel(
            name='Race',
        ),
    ]
