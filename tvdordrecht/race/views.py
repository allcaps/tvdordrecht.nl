# -*- coding: utf-8 -*-
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
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
from webapp.middleware import get_current_user

from .models import (
    Event,
    Distance,
    Result,
)
from .forms import (
    EditionSearchForm,
    EventForm,
    ResultForm,
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

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        now = timezone.now()
        event = context['object']
        context['www_list'] = Result.objects.filter(event=event, date__gt=now)
        context['result_list'] = Result.objects.filter(event=event, date__lte=now)
        return context

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
            .filter(date__gte=timezone.now())\
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
        queryset = queryset.filter(date__lte=timezone.now())
        return queryset


def get_help_text(name, url):
    template = """
        <p class="small">
            Staat jouw {name} niet in de lijst?
            <a href="{url}">+ {title} toevoegen</a>
        </p>
        """
    return template.format(name=name, url=url, title=name.title())


class WhoWhatWhereWizard(LoginRequiredMixin, CurrentMenuMixin,
                         SessionWizardView):
    template_name = 'race/who_what_where_wizard_form.html'
    success_message = "Succes: Wie Wat Waar is opgeslagen!"

    def get_form(self, step=None, data=None, files=None):
        form = super(WhoWhatWhereWizard, self).get_form(step, data, files)
        step = step or self.steps.current

        if step == '0':
            help_text = get_help_text('evenement', reverse("race:event_create"))
            form.fields['event'].help_text = help_text

        if step == '1':
            data = self.storage.get_step_data('0')
            event_pk = data.get('0-event')
            event = Event.objects.get(pk=event_pk)
            form.fields['date'].label = "Wanneer is %s?" % event.name
            form.fields['date'].help_text = "Format: DD-MM-YYYY"
            form.fields['user'].choices = [ (user.id, user.get_full_name()) for user in User.objects.all()]
            form.fields['user'].initial = get_current_user()

        return form

    def done(self, form_list, **kwargs):
        data = self.get_all_cleaned_data()
        distance = data['distance']

        if distance.id == 1:
            distance, created = Distance.objects.get_or_create(
                name=data['foo'],
                order='xx'
            )

        obj, created = Result.objects.get_or_create(
            user=self.request.user,
            event=data['event'],
            date=data['date'],
            distance=distance,
        )

        if created:
            messages.add_message(
                self.request,
                messages.SUCCESS,
                'Succes! Wie wat waar is opgeslagen.'
            )
        else:
            messages.add_message(
                self.request,
                messages.INFO,
                'Oeps! Er bestaat al een Wie wat waar voor %s %s %s %s.' %
                (obj.date, obj.event, obj.distance, obj.user.get_full_name())
            )

        if obj.date <= timezone.now().date():
            messages.add_message(
                self.request,
                messages.INFO,
                'Je kunt hier direct de uitslag doorgeven!'
            )
            return redirect(obj.get_edit_url())
        else:
            return redirect(obj.event.get_absolute_url())


class ResultUpdateView(LoginRequiredMixin, CurrentMenuMixin,
                       SuccessMessageMixin, UpdateView):
    model = Result
    form_class = ResultForm
    success_message = "Succes! Uitslag opgeslagen."


class ResultListAddView(LoginRequiredMixin, CurrentMenuMixin, ListView):
    model = Result
    template_name = 'race/result_list_add.html'

    def get_queryset(self):
        queryset = super(ResultListAddView, self).get_queryset()
        queryset = queryset.filter(date__lte=timezone.now(), time__isnull=True)
        return queryset
