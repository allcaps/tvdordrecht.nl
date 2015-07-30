# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('race', '0002_auto_20150729_1906'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='distance',
            options={'ordering': ['order'], 'verbose_name': 'Afstand', 'verbose_name_plural': 'Afstanden'},
        ),
        migrations.AlterModelOptions(
            name='result',
            options={'ordering': ['date', 'event', 'distance', 'time'], 'verbose_name': 'Wie wat waar / Uitslag', 'verbose_name_plural': 'Wie wat waars / Uitslagen'},
        ),
        migrations.RemoveField(
            model_name='distance',
            name='default',
        ),
        migrations.AddField(
            model_name='distance',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, verbose_name=b'laatst bewerkt', null=True),
        ),
        migrations.AddField(
            model_name='distance',
            name='last_modified_by',
            field=models.ForeignKey(related_name='distance_last_modified_by', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'Laatst bewerkt door'),
        ),
        migrations.AddField(
            model_name='distance',
            name='owner',
            field=models.ForeignKey(related_name='distance_owner', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'Eigenaar'),
        ),
        migrations.AddField(
            model_name='distance',
            name='pub_date',
            field=models.DateTimeField(null=True, verbose_name=b'publicatie datum', blank=True),
        ),
    ]
