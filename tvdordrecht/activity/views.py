# -*- coding: utf-8 -*-
from datetime import (
    datetime,
    timedelta,
)
from django.views.generic import (
    ListView,
    DetailView,
    FormView,
)
# from django.views.generic.detail import ContextMixin
# from django.db.models import Q
# from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from webapp.models import Menu
from .models import Activity

class CurrentMenuMixin(object):
    """ Adds the current menu to context data. """

    def get_context_data(self, **kwargs):
        context = super(CurrentMenuMixin, self).get_context_data(**kwargs)
        context['current_menu'] = get_object_or_404(Menu, slug='activiteiten')
        return context


class ActivityList(CurrentMenuMixin, ListView):
    model = Activity

class ActivityDetail(CurrentMenuMixin, DetailView):
    model = Activity