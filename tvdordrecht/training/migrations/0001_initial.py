# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('title', models.CharField(max_length=200, verbose_name=b'titel')),
                ('slug', models.SlugField(unique=True)),
                ('text', models.TextField(verbose_name=b'Omschrijving', blank=True)),
            ],
            options={
                'verbose_name': 'discipline',
                'verbose_name_plural': 'disciplines',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('title', models.CharField(max_length=200, verbose_name=b'titel')),
                ('address', models.CharField(max_length=200, verbose_name=b'adres')),
                ('city', models.CharField(max_length=200, verbose_name=b'plaats')),
                ('slug', models.SlugField(unique=True)),
                ('text', models.TextField(verbose_name=b'Omschrijving', blank=True)),
            ],
            options={
                'verbose_name': 'locatie',
                'verbose_name_plural': 'locaties',
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('start', models.DateTimeField(unique=True, verbose_name=b'Start')),
                ('message', models.CharField(help_text=b"Voor uitzonderingen ten opzichte van normaal. Bijvoorbeeld: 'Flippers menemen'.", max_length=400, verbose_name=b'Notificatie', blank=True)),
                ('cancel', models.BooleanField(default=False, help_text='Vink aan als de training afgelast is. Als afgelast, dan is een notificatie verplicht.', verbose_name='Afgelast')),
                ('discipline', models.ForeignKey(related_name='session_training', verbose_name=b'discipline', to='training.Discipline')),
                ('location', models.ForeignKey(related_name='session_location', verbose_name=b'locatie', blank=True, to='training.Location', null=True)),
                ('participants', models.ManyToManyField(related_name='session_participants', to=settings.AUTH_USER_MODEL, blank=True)),
                ('trainer', models.ForeignKey(related_name='session_trainer', verbose_name=b'trainer', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('start',),
                'verbose_name': 'trainingssessie',
                'verbose_name_plural': 'trainingssessies',
            },
        ),
        migrations.AlterUniqueTogether(
            name='session',
            unique_together=set([('start', 'discipline', 'location')]),
        ),
    ]
