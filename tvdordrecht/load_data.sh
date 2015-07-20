#!/bin/sh
python manage.py loaddata webapp/fixtures/menu.json --settings=settings.production
python manage.py loaddata webapp/fixtures/page.json --settings=settings.production
python manage.py loaddata webapp/fixtures/image.json --settings=settings.prodution
python manage.py loaddata webapp/fixtures/news.json --settings=settings.production
python manage.py loaddata race/fixtures/data.json --settings=settings.production
python manage.py loaddata swimtest/fixtures/data.json --settings=settings.production
