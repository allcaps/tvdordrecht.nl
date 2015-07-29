from django.conf.urls import patterns, include, url

from .views import (
    WhoWhatWhere,
    WhoWhatWhereWizard,
    ResultWizard,
    EventDetail,
    EventList,
    EventCreateView,
    EventUpdateView,
    ResultList,
)
from .forms import (
    WhoWhatWhereEventForm,
    # WhoWhatWhereEditionForm,
    # WhoWhatWhereRaceForm,
    ResultForm0,
    ResultForm1,
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
                # WhoWhatWhereEditionForm,
                # WhoWhatWhereRaceForm,
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
        ResultWizard.as_view(
            [
                ResultForm0,
                ResultForm1,
            ],
        ),
        name='result_add',
    ),
)
