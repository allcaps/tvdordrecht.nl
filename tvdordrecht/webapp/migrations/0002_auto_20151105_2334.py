# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_editing',
            field=models.CharField(default=b'', max_length=100, verbose_name=b'Afbeelding roteren', blank=True, choices=[('90', '90\xb0'), ('180', '180\xb0 '), ('270', '270\xb0'), ('double', 'Double the size')]),
        ),
        migrations.AlterField(
            model_name='image',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 5, 23, 32, 56, 361960), verbose_name=b'laatst bewerkt', auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='image',
            name='owner',
            field=models.ForeignKey(related_name='image_owner', verbose_name=b'gemaakt door', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 5, 23, 33, 1, 571704), verbose_name=b'publicatie datum', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='image',
            name='sortorder',
            field=models.IntegerField(help_text=b'\n    Als er meerdere afbeeldingen in een foto-album staan, worden ze standaard \n    op alfabetische volgorde weergeven. Om de volgorde te wijzigen geef je een \n    sortering (getal) bij alle te ordenen afbeeldigen in.\n    ', null=True, verbose_name=b'Sortering', blank=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='description',
            field=models.TextField(help_text=b'\n    Maximaal 250 karakters (Google zoekresultaten geven alleen de eerste 150 \n    karakters weer).<br>\n    Maak een relevante description. Bij voorkeur met tekst die op de pagina \n    voorkomt.</br>\n    Bij een leeg descriptionveld wordt description gegenereerd op basis van de \n    inhoud van het tekstveld.\n    ', max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='html',
            field=models.TextField(default='', verbose_name=b'html', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='menu',
            name='image',
            field=models.ForeignKey(related_name='menu_image', blank=True, to='webapp.Image', help_text=b'\n    Deze afbeelding komt op een vaste positie. Gebruik het afbeeldings-icoon\n    in de text-editor om afbeeldingen tussen de lopende tekst in te voegen.\n    ', null=True, verbose_name=b'afbeelding'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='keywords',
            field=models.TextField(help_text=b"\n    Alleen relevante keywords. Niet relevante keywords (die niet in de tekst \n    voorkomen) doen pagina's zakken.<br>\n    Bij een leeg keywordveld worden keywords gegenereerd op basis van de \n    inhoud van het tekstveld.\n    ", blank=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 5, 23, 33, 23, 947703), verbose_name=b'laatst bewerkt', auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='menu',
            name='owner',
            field=models.ForeignKey(related_name='menu_owner', verbose_name=b'gemaakt door', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 5, 23, 33, 28, 642875), verbose_name=b'publicatie datum', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='menu',
            name='table_of_contents',
            field=models.TextField(default='', verbose_name=b'table of contents', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='news',
            name='description',
            field=models.TextField(help_text=b'\n    Maximaal 250 karakters (Google zoekresultaten geven alleen de eerste 150 \n    karakters weer).<br>\n    Maak een relevante description. Bij voorkeur met tekst die op de pagina \n    voorkomt.</br>\n    Bij een leeg descriptionveld wordt description gegenereerd op basis van de \n    inhoud van het tekstveld.\n    ', max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ForeignKey(related_name='news_image', blank=True, to='webapp.Image', help_text=b'\n    Deze afbeelding komt op een vaste positie. Gebruik het afbeeldings-icoon\n    in de text-editor om afbeeldingen tussen de lopende tekst in te voegen.\n    ', null=True, verbose_name=b'afbeelding'),
        ),
        migrations.AlterField(
            model_name='news',
            name='keywords',
            field=models.TextField(help_text=b"\n    Alleen relevante keywords. Niet relevante keywords (die niet in de tekst \n    voorkomen) doen pagina's zakken.<br>\n    Bij een leeg keywordveld worden keywords gegenereerd op basis van de \n    inhoud van het tekstveld.\n    ", blank=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 5, 23, 33, 40, 588617), verbose_name=b'laatst bewerkt', auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='news',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 5, 23, 33, 46, 978172), verbose_name=b'publicatie datum', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='page',
            name='description',
            field=models.TextField(help_text=b'\n    Maximaal 250 karakters (Google zoekresultaten geven alleen de eerste 150 \n    karakters weer).<br>\n    Maak een relevante description. Bij voorkeur met tekst die op de pagina \n    voorkomt.</br>\n    Bij een leeg descriptionveld wordt description gegenereerd op basis van de \n    inhoud van het tekstveld.\n    ', max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='html',
            field=models.TextField(default='', verbose_name=b'html', editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='page',
            name='image',
            field=models.ForeignKey(related_name='page_image', blank=True, to='webapp.Image', help_text=b'\n    Deze afbeelding komt op een vaste positie. Gebruik het afbeeldings-icoon\n    in de text-editor om afbeeldingen tussen de lopende tekst in te voegen.\n    ', null=True, verbose_name=b'afbeelding'),
        ),
        migrations.AlterField(
            model_name='page',
            name='keywords',
            field=models.TextField(help_text=b"\n    Alleen relevante keywords. Niet relevante keywords (die niet in de tekst \n    voorkomen) doen pagina's zakken.<br>\n    Bij een leeg keywordveld worden keywords gegenereerd op basis van de \n    inhoud van het tekstveld.\n    ", blank=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 5, 23, 34, 1, 387628), verbose_name=b'laatst bewerkt', auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='page',
            name='owner',
            field=models.ForeignKey(related_name='page_owner', verbose_name=b'gemaakt door', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 5, 23, 34, 6, 421516), verbose_name=b'publicatie datum', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='page',
            name='table_of_contents',
            field=models.TextField(default='', verbose_name=b'table of contents', editable=False, blank=True),
            preserve_default=False,
        ),
    ]
