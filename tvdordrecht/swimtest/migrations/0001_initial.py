# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_100', models.TimeField(verbose_name='100 m')),
                ('time_200', models.TimeField(verbose_name='200 m')),
                ('time_300', models.TimeField(verbose_name='300 m')),
                ('time_400', models.TimeField(verbose_name='400 m')),
                ('time_500', models.TimeField(verbose_name='500 m')),
                ('split_100', models.TimeField(null=True, verbose_name='100 split', blank=True)),
                ('split_200', models.TimeField(null=True, verbose_name='200 split', blank=True)),
                ('split_300', models.TimeField(null=True, verbose_name='300 split', blank=True)),
                ('split_400', models.TimeField(null=True, verbose_name='400 split', blank=True)),
                ('split_500', models.TimeField(null=True, verbose_name='500 split', blank=True)),
                ('pace_time', models.TimeField(verbose_name='Pacetime', blank=True)),
                ('remarks', models.CharField(max_length=200, verbose_name=b'Opmerkingen', blank=True)),
            ],
            options={
                'ordering': ['pace_time'],
                'verbose_name': 'Testresultaat',
                'verbose_name_plural': 'Testresultaten',
            },
        ),
        migrations.CreateModel(
            name='SwimTest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'zwemtest',
                'verbose_name_plural': 'zwemtesten',
            },
        ),
        migrations.AddField(
            model_name='record',
            name='swim_test',
            field=models.ForeignKey(to='swimtest.SwimTest'),
        ),
        migrations.AddField(
            model_name='record',
            name='user',
            field=models.ForeignKey(verbose_name=b'Atleet', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='record',
            unique_together=set([('swim_test', 'user')]),
        ),
    ]
