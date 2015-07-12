from django.contrib.sites.models import Site

from .models import Menu


def basics(request):
    return {
        'menu': Menu.objects.all().prefetch_related('page'),
        'site': Site.objects.get_current(),
    }
