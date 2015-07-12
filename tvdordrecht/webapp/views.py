# -*- coding: utf-8 -*-
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import (
    get_object_or_404,
    render_to_response,
    redirect,
)
from django.template import RequestContext
from django.contrib import messages
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    YearArchiveView,
    TemplateView,
)

from .forms import (
    # NewsForm,
    ImageForm,
    ImageFormSet,
)
from .models import (
    Menu,
    Page,
    News,
    Image,
)
from training.models import Session
from datetime import datetime, timedelta

def home(request, template='webapp/home.html'):
    current_menu = get_object_or_404(Menu, slug='home')
    news_list = News.objects.filter(publish=True).order_by('-pub_date')[:6]
    now = datetime.now().date()
    then = now + timedelta(days=14)
    training_list = Session.objects \
        .filter(start__gte=now, start__lt=then) \
        .select_related('trainer', 'location', 'discipline')

    return render_to_response(
        template,
        context_instance=RequestContext(request, locals())
    )


def page(request, menu_slug, template='webapp/page.html'):
    current_menu = get_object_or_404(Menu, slug=menu_slug)
    articles = Page.objects.filter(menu=current_menu, publish=True)
    return render_to_response(
        template,
        context_instance=RequestContext(request, locals())
    )


def page_detail(request, article_slug, menu_slug, template='webapp/page_detail.html'):
    current_menu = get_object_or_404(Menu, slug=menu_slug)
    articles = Page.objects.filter(menu=current_menu, publish=True)
    article = get_object_or_404(articles, slug=article_slug, publish=True)
    return render_to_response(
        template,
        context_instance=RequestContext(request, locals())
    )


def logout(request):
    logout(request)
    return HttpResponseRedirect("/")


class CurrentMenuMixin(object):
    """ Adds the current menu object to the context data. """
    def get_context_data(self, **kwargs):
        context = super(CurrentMenuMixin, self).get_context_data(**kwargs)
        context['current_menu'] = get_object_or_404(Menu, slug='nieuws')
        return context


class YearListMixin(object):
    """ Adds a year list to the context data. """
    def get_context_data(self, **kwargs):
        context = super(YearListMixin, self).get_context_data(**kwargs)
        news = News.objects.filter(publish=True).order_by('-pub_date')
        year_list = []
        for i in news.datetimes('pub_date', 'year', order="DESC"):
            obj = {
                'count': news.filter(pub_date__year=i.year).count(),
                'title': i.year,
                'slug': i.year
            }
            if obj['count'] > 0:
                year_list.append(obj)
        context['year_list'] = year_list
        return context


class FlipperMixin(object):
    def get_context_data(self, **kwargs):
        context = super(FlipperMixin, self).get_context_data(**kwargs)
        context['prev'] = self.queryset.filter(pub_date__lt=context['object'].pub_date).first()
        context['next'] = self.queryset.filter(pub_date__gt=context['object'].pub_date).last()
        return context

from django.contrib.auth.decorators import login_required

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class NewsListView(CurrentMenuMixin, YearListMixin, ListView):
    queryset = News.objects.filter(publish=True)[:18]
    make_object_list = True


class NewsYearArchiveView(CurrentMenuMixin, YearListMixin, YearArchiveView):
    queryset = News.objects.filter(publish=True)
    date_field = "pub_date"
    make_object_list = True
    template_name = "webapp/news_list.html"


class NewsDetailView(CurrentMenuMixin, FlipperMixin, DetailView):
    queryset = News.objects.filter(publish=True)
    model = News


class FormsetMixin(object):
    object = None

    def get(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def get_formset_class(self):
        return self.formset_class

    def get_formset(self, formset_class):
        return formset_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        kwargs = {
            'instance': self.object
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        messages.success(self.request, 'Succes: Nieuwsbericht opgeslagen!')
        return redirect(reverse('webapp:news_list'))

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class NewsCreateView(LoginRequiredMixin, FormsetMixin, CreateView):
    template_name = 'webapp/news_form.html'
    model = Image
    form_class = ImageForm
    formset_class = ImageFormSet
    success_message = "Succes: Nieuwsbericht is opgeslagen!"


class NewsUpdateView(LoginRequiredMixin, FormsetMixin, UpdateView):
    template_name = 'webapp/news_form.html'
    is_update_view = True
    model = Image
    form_class = ImageForm
    formset_class = ImageFormSet
    success_message = "Succes: Nieuwsbericht is opgeslagen!"


from django.contrib.messages.views import SuccessMessageMixin
from forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages

class AccountCreateView(SuccessMessageMixin, CreateView):
    """
    Temp account registration form.
    """
    template_name = 'registration/account_form.html'
    form_class = UserForm

    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.create(
            username=data['username'],
            email=data['email'],
            is_staff=False,
            is_active=True,
            first_name=data['first_name'],
            last_name=data['last_name'],
        )
        user.set_password(data['password'])
        user.save()
        user = authenticate(username=user.username, password=data['password'])
        login(self.request, user)
        messages.success(
            self.request,
            "Je account is aangemaakt en je bent direct ingeloged. Welkom bij "
            "de Triathlonvereniging Dordrecht-website!"
        )
        return redirect(reverse('webapp:home'))

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'
