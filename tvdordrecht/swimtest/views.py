# -*- coding: utf-8 -*-
from django.db.models import Min
from django.views.generic import (
    ListView,
    DetailView,
)
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from webapp.models import Menu
from .models import (
    SwimTest,
    Record,
)
from .forms import (
    SwimTestSearchForm,
)

class CurrentMenuMixin(object):
    """ Adds the current menu object to the context data. """
    def get_context_data(self, **kwargs):
        context = super(CurrentMenuMixin, self).get_context_data(**kwargs)
        context['current_menu'] = get_object_or_404(Menu, slug='zwemtest')
        return context


class SwimTestList(CurrentMenuMixin, ListView):
    model = SwimTest

    def get_queryset(self, **kwargs):
        """ Filters the queryset with the search values. """
        queryset = super(SwimTestList, self).get_queryset()
        user = self.request.GET.get("user")
        if user:
            queryset = queryset.filter(record__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        """ Adds the search form to context data. """
        context = super(SwimTestList, self).get_context_data(**kwargs)
        initial_data = self.request.GET
        context['form'] = SwimTestSearchForm(initial=initial_data)
        return context


class SwimTestDetail(CurrentMenuMixin, DetailView):
    model = SwimTest


class UserList(CurrentMenuMixin, ListView):
    model = User
    template_name = 'swimtest/user_list.html'

    def get_queryset(self, **kwargs):
        queryset = super(UserList, self).get_queryset()
        queryset = queryset.order_by('username').exclude(record__isnull=True)
        return queryset


class UserDetail(CurrentMenuMixin, DetailView):
    model = User
    template_name = 'swimtest/user_detail.html'


class BestTimeList(CurrentMenuMixin, ListView):
    model = Record
    template_name = 'swimtest/best_time_list.html'

    def get_queryset(self, **kwargs):
        queryset = super(BestTimeList, self).get_queryset()\
            .order_by('user', 'time_500').distinct('user')
        ids = [obj.id for obj in queryset]
        queryset = self.model.objects.filter(pk__in=ids)\
            .select_related('user', 'swim_test').order_by('time_500')
        return queryset
