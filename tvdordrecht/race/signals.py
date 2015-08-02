from django.utils import timezone
from django.db.models.signals import pre_save

from webapp.middleware import get_current_user
from .models import (
    Event,
    Distance,
    Result,
)

def set_defaults(sender, instance, **kwargs):
    """ Give (meta) fields default values on model save. """
    if not instance.pub_date:
        instance.pub_date = timezone.now()
    if not instance.owner:
        instance.owner = get_current_user()
    instance.last_modified_by = get_current_user()

for model in [Event, Result, Distance]:
    pre_save.connect(set_defaults, sender=model)
