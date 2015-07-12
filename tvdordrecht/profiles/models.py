from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from model_utils.models import TimeStampedModel

#from django.contrib.auth.models import AbstractUser

class Profile(TimeStampedModel):
    """
    Profile model. Extension of the user model.
    """
    MALE = 'M'
    FEMALE = 'F'
    SEX_CHOICES = (
        (MALE, _('Male')),
        (FEMALE, _('Female')),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    text = models.TextField(_('text'), blank=True)
    birthday = models.DateField(_('birthday'))
    sex = models.CharField(_('sex'), max_length=1, choices=SEX_CHOICES)
    address = models.CharField(_('address'), max_length=200)
    postal_code = models.CharField(_('postal code'), max_length=200)
    city = models.CharField(_('city'), max_length=200)
    phone = models.CharField(_('telephone'), max_length=10, blank=True)
    mobile = models.CharField(_('mobile phone'), max_length=10, blank=True)
    bank_account = models.CharField(_('bank account'), max_length=200)
    ascription = models.CharField(
        _('ascription of the bank account'),
        max_length=200,
    )
    licence = models.BooleanField(_('athlete license'), default=False)

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
        ordering = ('user',)

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        view_name = "admin:%s_%s_change" % (content_type.app_label, content_type.model)
        url = urlresolvers.reverse(view_name, args=(self.id,))
        return url

    def get_absolute_url(self):
        return '/profile/%d/' % self.id


    # def get_previous(self):
    #     objects = self.__class__.objects.order_by('name').filter(title__lt=self.title).reverse()
    #     if objects:
    #         return objects[0]
    #     else:
    #         return None
    #
    # def get_next(self):
    #     objects = self.__class__.objects.order_by('name').filter(title__gt=self.title)
    #     if objects:
    #         return objects[0]
    #     else:
    #         return None

    def __unicode__(self):
        return self.user.username


# from django.db.models.signals import post_save
#
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#        profile, created = Profile.objects.get_or_create(user=instance)
#
# post_save.connect(create_user_profile, sender=User)


def get_absolute_url(self):
    return reverse('user', args=(self.id,))

User.add_to_class('get_absolute_url', get_absolute_url)
