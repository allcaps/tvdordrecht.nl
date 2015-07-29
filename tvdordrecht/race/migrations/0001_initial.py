# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Distance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('order', models.CharField(max_length=200, blank=True)),
                ('default', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['default', 'order'],
                'verbose_name': 'Afstand',
                'verbose_name_plural': 'Afstanden',
            },
        ),
        migrations.CreateModel(
            name='Edition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'editie',
                'verbose_name_plural': '  Edities',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200, verbose_name=b'Naam')),
                ('city', models.CharField(max_length=200, verbose_name=b'Plaats')),
                ('slug', models.SlugField(unique=True)),
                ('text', models.TextField(help_text=b'Korte omschrijving van dit evenement. Wat maakt dit evenement anders dan andere evenementen?', verbose_name=b'Tekst', blank=True)),
                ('website', models.URLField(help_text='Alleen de base url.', blank=True)),
                ('pub_date', models.DateTimeField(null=True, verbose_name=b'publicatie datum', blank=True)),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name=b'laatst bewerkt', null=True)),
                ('image', models.ForeignKey(verbose_name=b'event_image', blank=True, to='webapp.Image', null=True)),
                ('last_modified_by', models.ForeignKey(related_name='event_last_modified_by', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'Laatst bewerkt door')),
                ('owner', models.ForeignKey(related_name='event_owner', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'Eigenaar')),
            ],
            options={
                'verbose_name': 'evenement',
                'verbose_name_plural': '   Evenementen',
            },
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('distance', models.ForeignKey(to='race.Distance')),
                ('edition', models.ForeignKey(to='race.Edition')),
            ],
            options={
                'ordering': ['distance'],
                'verbose_name': 'wedstrijd',
                'verbose_name_plural': ' Wedstrijden',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.TimeField(help_text=b'HH:MM:SS', null=True, verbose_name=b'Tijd', blank=True)),
                ('remarks', models.CharField(help_text="Podiumplaatsen zijn het vermelden waard. Bijvoorbeeld: '1e H50'.", max_length=200, verbose_name=b'Opmerkingen', blank=True)),
                ('race', models.ForeignKey(verbose_name=b'Wedstrijd', to='race.Race')),
                ('user', models.ForeignKey(verbose_name=b'deelnemer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['race__edition', 'time'],
                'verbose_name': 'uitslag',
                'verbose_name_plural': 'uitslagen',
            },
        ),
        migrations.AddField(
            model_name='edition',
            name='event',
            field=models.ForeignKey(to='race.Event'),
        ),
        migrations.AlterUniqueTogether(
            name='result',
            unique_together=set([('user', 'race')]),
        ),
        migrations.AlterUniqueTogether(
            name='race',
            unique_together=set([('edition', 'distance')]),
        ),
        migrations.AlterUniqueTogether(
            name='edition',
            unique_together=set([('event', 'date')]),
        ),
    ]
