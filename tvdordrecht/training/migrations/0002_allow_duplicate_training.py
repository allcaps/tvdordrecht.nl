# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='start',
            field=models.DateTimeField(verbose_name=b'Start'),
        ),
        migrations.AlterUniqueTogether(
            name='session',
            unique_together=set([]),
        ),
    ]
