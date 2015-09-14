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
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(height_field=b'height', upload_to=b'images/%Y/%m/%d', width_field=b'width', verbose_name=b'afbeelding')),
                ('caption', models.CharField(max_length=600, verbose_name=b'bijschrift', blank=True)),
                ('sortorder', models.IntegerField(help_text=b'Als er meerdere afbeeldingen in een foto-album staan, worden ze standaard op alfabetische volgorde weergeven. Om de volgorde te wijzigen geef je een sortering (getal) bij alle te ordenen afbeeldigen in.', null=True, verbose_name=b'Sortering', blank=True)),
                ('height', models.IntegerField(editable=False, blank=True)),
                ('width', models.IntegerField(editable=False, blank=True)),
                ('image_editing', models.CharField(default=b'', max_length=100, verbose_name=b'Afbeelding roteren', blank=True, choices=[('90', '90\xb0'), ('180', '180\xb0 '), ('270', '270\xb0'), ('double', 'Double the size!')])),
                ('pub_date', models.DateTimeField(null=True, verbose_name=b'publicatie datum', blank=True)),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name=b'laatst bewerkt', null=True)),
                ('last_modified_by', models.ForeignKey(related_name='image_last_modified_by', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'Laatst bewerkt door')),
                ('owner', models.ForeignKey(related_name='image_owner', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'Eigenaar')),
            ],
            options={
                'ordering': ['-pub_date'],
                'verbose_name': 'Afbeelding',
                'verbose_name_plural': 'Afbeeldingen',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name=b'titel')),
                ('text', models.TextField(verbose_name=b'tekst', blank=True)),
                ('html', models.TextField(verbose_name=b'html', null=True, editable=False, blank=True)),
                ('table_of_contents', models.TextField(verbose_name=b'table of contents', null=True, editable=False, blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('sortorder', models.IntegerField(null=True, verbose_name=b'sortering', blank=True)),
                ('pub_date', models.DateTimeField(null=True, verbose_name=b'publicatie datum', blank=True)),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name=b'laatst bewerkt', null=True)),
                ('keywords', models.TextField(help_text=b"Alleen relevante keywords. Niet relevante keywords (die niet in de tekst voorkomen) doen pagina's zakken.<br>\n                        Bij een leeg keywordveld worden keywords gegenereerd op basis van de inhoud van het tekstveld.", blank=True)),
                ('description', models.TextField(help_text=b'Maximaal 250 karakters (Google zoekresultaten geven alleen de eerste 150 karakters weer).<br>\n                            Maak een relevante description. Bij voorkeur met tekst die op de pagina voorkomt.</br>\n                            Bij een leeg descriptionveld wordt description gegenereerd op basis van de inhoud van het tekstveld.', max_length=250, blank=True)),
                ('image', models.ForeignKey(related_name='menu_image', blank=True, to='webapp.Image', help_text=b'Deze afbeelding komt op een vaste positie. Gebruik het afbeeldings-icoon in de text-editor om afbeeldingen tussen de lopende tekst in te voegen.', null=True, verbose_name=b'afbeelding')),
                ('last_modified_by', models.ForeignKey(related_name='menu_last_modified_by', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'Laatst bewerkt door')),
                ('owner', models.ForeignKey(related_name='menu_owner', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'Eigenaar')),
            ],
            options={
                'ordering': ('sortorder',),
                'verbose_name': 'menu-item',
                'verbose_name_plural': 'menu',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name=b'titel')),
                ('text', models.TextField(verbose_name=b'tekst')),
                ('slug', models.SlugField(unique=True)),
                ('publish', models.BooleanField(default=True, verbose_name=b'publiceren')),
                ('pub_date', models.DateTimeField(null=True, verbose_name=b'publicatie datum', blank=True)),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name=b'laatst bewerkt', null=True)),
                ('keywords', models.TextField(help_text=b"Alleen relevante keywords. Niet relevante keywords (die niet in de tekst voorkomen) doen pagina's zakken.<br>\n                        Bij een leeg keywordveld worden keywords gegenereerd op basis van de inhoud van het tekstveld.", blank=True)),
                ('description', models.TextField(help_text=b'Maximaal 250 karakters (Google zoekresultaten geven alleen de eerste 150 karakters weer).<br>\n                            Maak een relevante description. Bij voorkeur met tekst die op de pagina voorkomt.</br>\n                            Bij een leeg descriptionveld wordt description gegenereerd op basis van de inhoud van het tekstveld.', max_length=250, blank=True)),
                ('image', models.ForeignKey(related_name='news_image', blank=True, to='webapp.Image', help_text=b'Deze afbeelding komt op een vaste positie. Gebruik het afbeeldings-icoon in de text-editor om afbeeldingen tussen de lopende tekst in te voegen.', null=True, verbose_name=b'afbeelding')),
                ('last_modified_by', models.ForeignKey(related_name='news_last_modified_by', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'Laatst bewerkt door')),
                ('owner', models.ForeignKey(related_name='news_owner', verbose_name=b'gemaakt door', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-pub_date'],
                'verbose_name': 'nieuws-item',
                'verbose_name_plural': 'nieuws',
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name=b'titel')),
                ('text', models.TextField(verbose_name=b'tekst', blank=True)),
                ('html', models.TextField(verbose_name=b'html', null=True, editable=False, blank=True)),
                ('table_of_contents', models.TextField(verbose_name=b'table of contents', null=True, editable=False, blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('publish', models.BooleanField(default=True, verbose_name=b'publiceren')),
                ('sortorder', models.IntegerField(null=True, verbose_name=b'sortering', blank=True)),
                ('pub_date', models.DateTimeField(verbose_name=b'publicatie datum', null=True, editable=False, blank=True)),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name=b'laatst bewerkt', null=True)),
                ('keywords', models.TextField(help_text=b"Alleen relevante keywords. Niet relevante keywords (die niet in de tekst voorkomen) doen pagina's zakken.<br>\n                        Bij een leeg keywordveld worden keywords gegenereerd op basis van de inhoud van het tekstveld.", blank=True)),
                ('description', models.TextField(help_text=b'Maximaal 250 karakters (Google zoekresultaten geven alleen de eerste 150 karakters weer).<br>\n                            Maak een relevante description. Bij voorkeur met tekst die op de pagina voorkomt.</br>\n                            Bij een leeg descriptionveld wordt description gegenereerd op basis van de inhoud van het tekstveld.', max_length=250, blank=True)),
                ('image', models.ForeignKey(related_name='page_image', blank=True, to='webapp.Image', help_text=b'Deze afbeelding komt op een vaste positie. Gebruik het afbeeldings-icoon in de text-editor om afbeeldingen tussen de lopende tekst in te voegen.', null=True, verbose_name=b'afbeelding')),
                ('last_modified_by', models.ForeignKey(related_name='page_last_modified_by', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'Laatst bewerkt door')),
                ('menu', models.ForeignKey(related_name='page', to='webapp.Menu')),
                ('owner', models.ForeignKey(related_name='page_owner', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'Eigenaar')),
            ],
            options={
                'ordering': ('sortorder', 'title'),
                'verbose_name': 'pagina',
                'verbose_name_plural': "pagina's",
            },
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together=set([('menu', 'slug')]),
        ),
    ]
