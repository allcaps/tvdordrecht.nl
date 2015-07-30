from django.utils import timezone

from django.db.models.signals import pre_save
from django.utils.text import slugify

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
    # Maybe this should live in the forms save method.
    # Because slug is a required field.
    if instance == Event and not instance.slug:
        instance.slug = slugify("%s %s" % (instance.name, instance.city))


for model in [Event, Result, Distance]:
    pre_save.connect(set_defaults, sender=model)
