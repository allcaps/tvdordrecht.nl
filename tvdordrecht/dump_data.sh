#!/bin/sh
python manage.py dumpdata django.contrib.auth --indent=4 > tvdordrecht/fixtures/auth.json
python manage.py dumpdata django.contrib.auth.User --indent=4 > tvdordrecht/fixtures/user.json
python manage.py dumpdata django.contrib.sites.Site --indent=4 > tvdordrecht/fixtures/site.json

python manage.py dumpdata webapp --indent=4 > webapp/fixtures/data.json
python manage.py dumpdata webapp.Menu --indent=4 > webapp/fixtures/menu.json
python manage.py dumpdata webapp.Page --indent=4 > webapp/fixtures/page.json
python manage.py dumpdata webapp.Image --indent=4 > webapp/fixtures/image.json
python manage.py dumpdata webapp.News --indent=4 > webapp/fixtures/news.json

python manage.py dumpdata race --indent=4 > race/fixtures/data.json
python manage.py dumpdata race.Event --indent=4 > race/fixtures/event.json
python manage.py dumpdata race.Edition --indent=4 > race/fixtures/edition.json
python manage.py dumpdata race.Distance --indent=4 > race/fixtures/distance.json
python manage.py dumpdata race.Serie --indent=4 > race/fixtures/serie.json
python manage.py dumpdata race.Result --indent=4 > race/fixtures/result.json

python manage.py dumpdata trianing --indent=4 > training/fixtures/data.json
python manage.py dumpdata trianing.Discipline --indent=4 > training/fixtures/discipline.json
python manage.py dumpdata trianing.Session --indent=4 > training/fixtures/session.json
python manage.py dumpdata trianing.Location --indent=4 > training/fixtures/location.json

python manage.py dumpdata zwemtest --indent=4 > zwemtest/fixtures/data.json
python manage.py dumpdata zwemtest.SwimTest --indent=4 > zwemtest/fixtures/swimtest.json
python manage.py dumpdata zwemtest.Record --indent=4 > zwemtest/fixtures/record.json