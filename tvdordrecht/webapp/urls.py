# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import (
    NewsCreateView,
    NewsDetailView,
    NewsListView,
    NewsUpdateView,
    NewsYearArchiveView,
    AccountCreateView,
    ProfileView,
    home,
    page,
    page_detail,
    logout,
)

urlpatterns = [
    url(
        r'^$',
        home,
        name='home',
    ),
    url(
        r'^nieuws/toevoegen/$',
        NewsCreateView.as_view(),
        name='news_create',
    ),
    url(
        r'^nieuws/$',
        NewsListView.as_view(),
        name='news_list',
    ),
    url(
        r'^nieuws/(?P<year>\d{4})/$',
        NewsYearArchiveView.as_view(),
        name='news_list',
    ),
    url(
        r'^nieuws/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<pk>\d+)/(?P<slug>[A-Za-z0-9-_]+)/$',
        NewsDetailView.as_view(),
        name='news_detail',
    ),
    url(
        r'^nieuws/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<news_pk>\d+)/(?P<slug>[A-Za-z0-9-_]+)/(?P<pk>\d+)/bewerken/$',
        NewsUpdateView.as_view(),
        name='news_update',
    ),
    url(
        r'^logout/$',
        logout,
        name='logout',
    ),
    url(
        r'^account-aanmaken/$',
        AccountCreateView.as_view(),
        name='account_create',
    ),
    url(
        r'^profiel/$',
        ProfileView.as_view(),
        name='profile',
    ),
    url(
        r'^(?P<menu_slug>[A-Za-z0-9-_]+)/$',
        page,
        name='menu',
    ),
    url(
        r'^(?P<menu_slug>[A-Za-z0-9-_]+)/(?P<article_slug>[A-Za-z0-9-_]+)/$',
        page_detail,
        name='page_detail',
    ),

]
