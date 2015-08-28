from django.utils import timezone

from django.db.models.signals import pre_save
from django.utils.text import slugify

from .middleware import get_current_user
from .models import (
    Menu,
    Page,
    Image,
    News,
)
from .utils import (
    get_description,
    make_table,
    obfuscate_email,
)


def set_defaults(sender, instance, **kwargs):
    """ Give (meta) fields default values on model save. """
    if not instance.pub_date:
        instance.pub_date = timezone.now()
    # TODO: I don't trust get_current_user. So this try and except it temp hack.
    try:
        if not instance.owner:
            instance.owner = get_current_user()
        instance.last_modified_by = get_current_user()
    except:
        pass
    if not sender == Image and not instance.description:
        instance.description = get_description(instance.text)
    if hasattr(instance, 'table_of_contents'):
        instance.table_of_contents, instance.html = make_table(instance.text)
        instance.html = obfuscate_email(instance.html)
    if sender is News and not instance.slug:
        slug = slugify(instance.title)
        num = 1
        while News.objects.filter(slug=slug).count():
            slug = "%s-%d" %(slugify(instance.title), num)
            num += 1
        instance.slug = slug

for model in [Menu, Page, Image, News]:
    pre_save.connect(set_defaults, sender=model)
