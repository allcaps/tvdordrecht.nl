from django.conf.urls import patterns, url

from .views import (
    UserList,
    UserDetail,
    ProfileFormView,
    )

urlpatterns = patterns('',
    url(
        r'^$',
        UserList.as_view(),
        name='user-list',
    ),
    url(
        r'^(?P<pk>[0-9]+)/$',
        UserDetail.as_view(),
        name='user',
    ),
    url(
        r'^profiel/$',
        ProfileFormView.as_view(),
        name='profile-form',
    ),
)
