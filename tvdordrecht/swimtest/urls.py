from django.conf.urls import patterns, url

from .views import (
    SwimTestList,
    SwimTestDetail,
    UserDetail,
    UserList,
    BestTimeList,
    )

urlpatterns = patterns('',
    url(
        r'^besttijden/$',
        BestTimeList.as_view(),
        name='best-time-list',
    ),
    url(
        r'^deelnemers/$',
        UserList.as_view(),
        name='user-list',
    ),
    url(
        r'^deelnemers/(?P<pk>[0-9]+)/$',
        UserDetail.as_view(),
        name='swimtest-user',
    ),
    url(
        r'^zwemtesten/$',
        SwimTestList.as_view(),
        name='swim-test-list',
    ),
    url(
        r'^zwemtesten/(?P<pk>[0-9]+)/$',
        SwimTestDetail.as_view(),
        name='swim-test',
    ),
)
