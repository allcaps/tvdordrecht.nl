from django.conf.urls import patterns, url

from .views import (
    SessionList,
    SessionDetail,
    DisciplineList,
    LocationList,
)

urlpatterns = patterns('',
    url(
        r'^$',
        SessionList.as_view(),
        name='session_list',
    ),
    url(
        r'^disciplines/$',
        DisciplineList.as_view(),
        name='discipline_list',
    ),
    url(
        r'^locaties/$',
        LocationList.as_view(),
        name='location_list',
    ),
    url(
        r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<pk>[A-Za-z0-9-_]+)/$',
        SessionDetail.as_view(),
        name='session',
    ),
)
