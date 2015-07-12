from django.conf.urls import patterns, url

from .views import (
    ActivityList,
    ActivityDetail,
    )

urlpatterns = patterns('',
    url(
        r'^$',
        ActivityList.as_view(),
        name='activity-list',
    ),
    url(
        r'^(?P<pk>[0-9]+)/$',
        ActivityDetail.as_view(),
        name='activity',
    ),
)
