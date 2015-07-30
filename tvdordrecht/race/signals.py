from django.utils import timezone

from django.db.models.signals import pre_save
from django.utils.text import slugify

from webapp.middleware import get_current_user
from .models import (
    Event,
    Result
)


def set_event_fields(sender, instance, **kwargs):
    """ Give (meta) fields default values on model save. """
    if not instance.pub_date:
        instance.pub_date = timezone.now()
    if not instance.slug:
        instance.slug = slugify("%s %s" % (instance.name, instance.city))
    if not instance.owner:
        instance.owner = get_current_user()
    instance.last_modified_by = get_current_user()

pre_save.connect(set_event_fields, sender=Event)


def set_result_fields(sender, instance, **kwargs):
    """ Give (meta) fields default values on model save. """
    if not instance.owner:
        instance.owner = get_current_user()
    instance.last_modified_by = get_current_user()

pre_save.connect(set_result_fields, sender=Result)
