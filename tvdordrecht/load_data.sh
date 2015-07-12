#!/bin/sh
python manage.py loaddata webapp/fixtures/menu.json
python manage.py loaddata webapp/fixtures/page.json
python manage.py loaddata webapp/fixtures/image.json
python manage.py loaddata webapp/fixtures/news.json
python manage.py loaddata race/fixtures/data.json
python manage.py loaddata swimtest/fixtures/data.json