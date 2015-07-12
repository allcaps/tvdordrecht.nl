from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin


admin.autodiscover()



urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^wedstrijd/', include('race.urls', namespace="race")),
    url(r'^training/', include('training.urls', namespace="training")),
    url(r'^zwemtest/', include('swimtest.urls')),
    url(r'^leden/', include('profiles.urls')),
    url(r'^', include('webapp.urls', namespace="webapp")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += patterns('',
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     )
