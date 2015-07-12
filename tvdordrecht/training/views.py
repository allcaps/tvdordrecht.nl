# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.views.generic import (
    ListView,
    DetailView,
    FormView,
    )
from django.shortcuts import get_object_or_404

from webapp.models import Menu

from .models import (
    Session,
    Location,
    Discipline,
)


class CurrentMenuMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CurrentMenuMixin, self).get_context_data(**kwargs)
        context['current_menu'] = get_object_or_404(Menu, slug='training')
        return context


class SessionList(CurrentMenuMixin, ListView):
    model = Session

    def get_queryset(self, **kwargs):
        now = datetime.now().date()
        then = now + timedelta(days=90)
        queryset = super(SessionList, self).get_queryset() \
            .filter(start__gte=now, start__lt=then) \
            .select_related('trainer', 'location', 'discipline')
        return queryset


class SessionDetail(CurrentMenuMixin, DetailView):
    model = Session


class DisciplineList(CurrentMenuMixin, ListView):
    model = Discipline

class LocationList(CurrentMenuMixin, ListView):
    model = Location
