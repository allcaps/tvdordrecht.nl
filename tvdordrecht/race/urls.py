from django.conf.urls import patterns, url

from .views import (
    WhoWhatWhere,
    WhoWhatWhereWizard,
    EventDetail,
    EventList,
    EventCreateView,
    EventUpdateView,
    ResultList,
    ResultListAddView,
    ResultUpdateView,
)
from .forms import (
    WhoWhatWhereEventForm,
    WhoWhatWhereDetailForm,
)


urlpatterns = patterns('',
    url(
        r'^evenementen/$',
        EventList.as_view(),
        name='event_list',
    ),
    url(
        r'^evenementen/toevoegen/$',
        EventCreateView.as_view(),
        name='event_create',
    ),
    url(
        r'^evenementen/(?P<slug>[A-Za-z0-9-_]+)/$',
        EventDetail.as_view(),
        name='event_detail',
    ),
    url(
        r'^evenementen/(?P<slug>[A-Za-z0-9-_]+)/bewerken/$',
        EventUpdateView.as_view(),
        name='event_update',
    ),
    url(
        r'^wie-wat-waar/$',
        WhoWhatWhere.as_view(),
        name='who_what_where_list',
    ),
    url(
        r'^wie-wat-waar/toevoegen/$',
        WhoWhatWhereWizard.as_view(
            [
                WhoWhatWhereEventForm,
                WhoWhatWhereDetailForm,
            ],
        ),
        name='who_what_where_add',
    ),
    url(
        r'^uitslagen/$',
        ResultList.as_view(),
        name='result_list',
    ),
    url(
        r'^uitslagen/toevoegen/$',
        ResultListAddView.as_view(),
        name='result_list_add',
    ),
    url(
        r'^uitslagen/(?P<pk>\d+)/$',
        ResultUpdateView.as_view(),
        name='result_update',
    ),
)
