# -*- coding: utf-8 -*-
from datetime import datetime

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from formtools.wizard.views import SessionWizardView
from django.db.models import Q
from django.shortcuts import get_object_or_404

from webapp.models import (
    Menu,
    Page,
)

from .models import (
    Event,
    Result,
)
from .forms import (
    EditionSearchForm,
    EventForm,
)

from django.contrib.auth.decorators import login_required

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(*args, **kwargs)
        return login_required(view)


class CurrentMenuMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CurrentMenuMixin, self).get_context_data(**kwargs)
        context['current_menu'] = get_object_or_404(Menu, slug='wedstrijd')
        return context


class CurrentPageMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CurrentPageMixin, self).get_context_data(**kwargs)
        context['object'] = get_object_or_404(Page, slug=self.page_slug)
        return context


class EventList(CurrentMenuMixin, CurrentPageMixin, ListView):
    model = Event
    page_slug = 'evenementen'


class EventDetail(CurrentMenuMixin, DetailView):
    model = Event


class EventCreateView(LoginRequiredMixin, CurrentMenuMixin, SuccessMessageMixin, CreateView):
    template_name = 'race/event_form.html'
    model = Event
    form_class = EventForm
    success_message = "Succes: %(name)s is opgeslagen!"


class EventUpdateView(LoginRequiredMixin, CurrentMenuMixin, SuccessMessageMixin, UpdateView):
    template_name = 'race/event_form.html'
    is_update_view = True
    model = Event
    form_class = EventForm
    success_message = "Succes: %(name)s is opgeslagen!"


class CurrentEventMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CurrentEventMixin, self).get_context_data(**kwargs)
        context['event'] = get_object_or_404(Event, slug=self.kwargs.get('event_slug'))
        return context


class WhoWhatWhere(CurrentMenuMixin, CurrentPageMixin, ListView):
    model = Result
    template_name = 'race/who_what_where_list.html'
    page_slug = 'wie-wat-waar'

    def get_queryset(self, **kwargs):
        """Filters the queryset with the search values."""
        queryset = Result.objects.filter(time=None)\
            .filter(date__gte=datetime.now())\
            .order_by('-date', 'distance', 'user')

        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(
                Q(event__name__contains=q) |
                Q(event__city__contains=q) |
                Q(user__username=q)
            )
        user = self.request.GET.get("user")
        if user:
            queryset = queryset.filter(user=user)

        return queryset

    def get_context_data(self, **kwargs):
        """Adds the search form to context data"""
        context = super(WhoWhatWhere, self).get_context_data(**kwargs)
        initial_data = self.request.GET
        context['form'] = EditionSearchForm(initial=initial_data)
        return context


class ResultList(CurrentMenuMixin, CurrentPageMixin, ListView):
    model = Result
    page_slug = 'uitslagen'

    def get_queryset(self):
        queryset = super(ResultList, self).get_queryset()
        now = datetime.now()
        queryset = queryset.filter(time__isnull=False,
                                   date__lte=now)
        return queryset


def get_help_text(name, url):
    template = """
        <p class="small">
            Staat jouw {name} niet in de lijst?
            <a href="{url}">+ {title} toevoegen</a>
        </p>
        """
    return template.format(name=name, url=url, title=name.title())


class WhoWhatWhereWizard(LoginRequiredMixin, CurrentMenuMixin, SuccessMessageMixin, SessionWizardView):
    template_name = 'race/who_what_where_wizard_form.html'
    success_message = "Succes: Wie Wat Waar is opgeslagen!"

    def get_form(self, step=None, data=None, files=None):
        form = super(WhoWhatWhereWizard, self).get_form(step, data, files)
        step = step or self.steps.current

        if step == '0':
            help_text = get_help_text('evenement', reverse("race:event_create"))
            form.fields['event'].help_text = help_text

        if step in ['1', '2']:
            data = self.storage.get_step_data('0')
            event_pk = data.get('0-event')
            event = Event.objects.get(pk=event_pk)

            if step == '1':
                form.fields['edition'].queryset = event.edition_set.all()
                help_text = get_help_text('editie', reverse(
                    "race:edition_create", kwargs={'event_slug': event.slug}))
                form.fields['edition'].help_text = help_text

            # if step == '2':
            #     data = self.storage.get_step_data('1')
            #     edition = Edition.objects.get(pk=data.get('1-edition'))
            #     qs = edition.race_set.all()
            #     form.fields['race'].queryset = qs
            #     initial = [i.race.pk for i in self.request.user.result_set.all()]
            #     form.fields['race'].initial = initial
            #     help_text = get_help_text('wedstrijd', reverse(
            #         "race:edition_update", kwargs={'event_slug': event.slug,
            #                                        'pk': edition.pk}))
            #     form.fields['race'].help_text = help_text
        return form

    def done(self, form_list, **kwargs):
        # TODO: Remove edition.results time==Null before saving the new Results.
        for race in self.get_all_cleaned_data()['race']:
            Result.objects.get_or_create(
                user=self.request.user,
                race=race
            )
        return redirect(reverse("race:who_what_where_list"))


class ResultWizard(LoginRequiredMixin, CurrentMenuMixin, SuccessMessageMixin, SessionWizardView):
    template_name = 'race/result_wizard_form.html'
    success_message = "Succes: Resultaat is opgeslagen!"

    def get_form(self, step=None, data=None, files=None):
        form = super(ResultWizard, self).get_form(step, data, files)
        step = step or self.steps.current

        if step == '0':
            results = self.request.user.result_set.filter(
                time__isnull=True, date__lte=datetime.now()
            )
            choices = [(res.id, res.choice_label) for res in results]
            form.fields['result'].choices = choices
            form.fields['result'].help_text = """
            <p class="small">
                Staat jouw wedstrijd niet in deze lijst?
                <a href="%s">+ Wie wat waar toevoegen</a>
            </p>
            """ % reverse('race:who_what_where_add')
        return form

    def done(self, form_list, **kwargs):
        data = self.get_all_cleaned_data()
        result = Result.objects.get(pk=data['result'])
        result.time = data['time']
        result.remarks = data['remarks']
        result.save()
        return redirect(reverse("race:result_list"))
