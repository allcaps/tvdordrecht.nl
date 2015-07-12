# -*- coding: utf-8 -*-
from django.db.models import Min
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
)
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from webapp.models import Menu
from .models import Profile
from .forms import ProfileForm


class CurrentMenuMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CurrentMenuMixin, self).get_context_data(**kwargs)
        context['current_menu'] = get_object_or_404(Menu, slug='leden')
        return context


class UserList(CurrentMenuMixin, ListView):
    model = User
    template_name = 'profiles/user_list.html'

    def get_queryset(self, **kwargs):
        queryset = super(UserList, self).get_queryset() \
            .order_by('username')
        return queryset

    # def get_queryset(self, **kwargs):
    #     queryset = super(UserList, self).get_queryset()
    #     user = self.request.GET.get("user")
    #     if user:
    #         queryset = queryset.filter(record__user=user)
    #     return queryset
    #
    # def get_context_data(self, **kwargs):
    #     context = super(UserList, self).get_context_data(**kwargs)
    #     initial_data = self.request.GET
    #     context['form'] = USerSearchForm(initial=initial_data)
    #     return context


class UserDetail(CurrentMenuMixin, DetailView):
    model = User
    template_name = 'profiles/user_detail.html'


class ProfileFormView(CurrentMenuMixin, UpdateView):
    #model = Profile
    form_class = ProfileForm
    template_name = 'profiles/profile_form.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileFormView, self).get_context_data(**kwargs)
        initial_data = get_object_or_404(Profile, user=self.request.user)
        context['form'] = ProfileForm(initial=initial_data)
        import pdb; pdb.set_trace()
        return context
