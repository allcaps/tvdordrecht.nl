from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from profiles.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiel'


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_filter = ['is_staff', 'is_active', 'is_superuser']
    list_display = ['username', 'first_name', 'last_name', 'is_active',
        'last_login']

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(Profile, ProfileAdmin)
