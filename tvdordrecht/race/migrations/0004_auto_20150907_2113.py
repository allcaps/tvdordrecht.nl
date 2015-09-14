# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('race', '0003_auto_20150730_2250'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['name', 'city'], 'verbose_name': 'evenement', 'verbose_name_plural': 'evenementen'},
        ),
        migrations.AlterModelOptions(
            name='result',
            options={'ordering': ['-date', 'event', 'distance', 'time'], 'verbose_name': 'Wie wat waar / Uitslag', 'verbose_name_plural': 'Wie wat waars / Uitslagen'},
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(help_text=b"De naam van dit evenement. Bijvoorbeeld: 'Triathlon Binnenmaas'", unique=True, max_length=200, verbose_name=b'Naam'),
        ),
        migrations.AlterField(
            model_name='result',
            name='date',
            field=models.DateField(help_text=b'YYYY-MM-DD', verbose_name=b'datum'),
        ),
        migrations.AlterField(
            model_name='result',
            name='distance',
            field=models.ForeignKey(verbose_name=b'Afstand', to='race.Distance'),
        ),
        migrations.AlterField(
            model_name='result',
            name='event',
            field=models.ForeignKey(verbose_name=b'Evenement', to='race.Event'),
        ),
        migrations.AlterField(
            model_name='result',
            name='time',
            field=models.TimeField(help_text='Format: UU:MM:SS. Bijvoorbeeld: 00:20:05 (twintig minuten en vijf seconden).', null=True, verbose_name=b'Tijd', blank=True),
        ),
    ]
