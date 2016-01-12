from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = [
    # We closed registration. So here we highjack the create account url
    # Direct to template won't do anyting with http post.
    url('^account-aanmaken/$',
        TemplateView.as_view(template_name='registration/account_form.html'),),
    url('^', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^wedstrijd/', include('race.urls', namespace="race")),
    url(r'^training/', include('training.urls', namespace="training")),
    url(r'^zwemtest/', include('swimtest.urls')),
    url(r'^', include('webapp.urls', namespace="webapp")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
