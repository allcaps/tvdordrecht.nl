# -*- coding: utf-8 -*-
from datetime import (
    timedelta,
    )

from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.template import defaultfilters
from django.utils.translation import ugettext_lazy as _

from .models import (
    Discipline,
    Location,
    Session,
)


def remove(modeladmin, request, queryset):
    queryset.delete()
remove.short_description = "Verwijderen"


def go_on(modeladmin, request, queryset):
    queryset.update(cancel=False)
go_on.short_description = "Gaat door (zet agelast uit)"


def duplicate(modeladmin, request, queryset):
    """
    Duplicate action.
    Duplicates each item in the queryset to the next week.
    Skips to the next week if a similar object already exists.
    """
    for i in queryset:
        created = False
        offset = timedelta()
        while not created:
            offset += timedelta(weeks=1)
            try:
                obj = Session.objects.get(start=i.start + offset)
            except Session.DoesNotExist:
                obj = Session(
                    start=i.start + offset,
                    discipline=i.discipline,
                    location=i.location,
                )
            for attr in ['trainer', 'message']:
                setattr(obj, attr, i.__getattribute__(attr))
            obj.save()
            created = True

duplicate.short_description = "Dupliceer"


def duplicate12(modeladmin, request, queryset):
    """ Duplicate 12 action.
        Duplicates each item in the queryset to the next week.
        Continues duplicating until 12 duplicates are created.
        Skips to the next week if a similar object already exists.
    """
    for i in queryset:
        count = 0
        offset = timedelta()
        while count < 12:
            created = False
            while not created:
                offset += timedelta(weeks=1)
                try:
                    obj = Session.objects.get(start=i.start + offset)
                except Session.DoesNotExist:
                    obj = Session(
                        start=i.start + offset,
                        discipline=i.discipline,
                        location=i.location,
                    )
                for attr in ['trainer', 'message']:
                    setattr(obj, attr, i.__getattribute__(attr))
                obj.save()
                count += 1
                created = True

duplicate12.short_description = "Dupliceer 12 keer"


class DisciplineAdmin(admin.ModelAdmin):
    list_display = ['title', ]
    prepopulated_fields = {'slug': ('title', )}
    fieldsets = (
            (None, {
                'fields': ('title', 'text'),
            }),
            ('Geavanceerde opties', {
                'classes': ('collapse',),
                'fields': ('slug', )
            }),
        )

admin.site.register(Discipline, DisciplineAdmin)

ckeditor = ['/static/webapp/ckeditor/ckeditor.js','/static/webapp/ckeditor.init.js']
ckeditor_css = ['/static/webapp/webapp.css']

class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', 'city')}

    class Media:
        js = ckeditor

admin.site.register(Location, LocationAdmin)


class SessionAdminForm(forms.ModelForm):

    participants = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        )

    def __init__(self, *args, **kwargs):
        super(SessionAdminForm, self).__init__(*args, **kwargs)
        self.fields['participants'].queryset = User.objects.all()

    class Meta:
        model = Session
        exclude = []

    def clean(self):
        data = self.cleaned_data
        if not data['location'] and not data['message']:
            raise forms.ValidationError(
                u"Selecteer een locatie of voeg een notificatie toe."
                )
        if data['cancel'] and not data['message']:
            raise forms.ValidationError(
                u"Voeg een notificatie toe."
                )
        return self.cleaned_data


def session_title(obj):
    return ("%s %s" % (
        defaultfilters.date(obj.start, "l"),
        defaultfilters.date(obj.start, "DATETIME_FORMAT"),
        )
    )

session_title.short_description = 'Datum en tijd'
session_title.admin_order_field = 'start'

def status(obj):
    return not obj.cancel

status.short_description = 'Gaat door'
status.admin_order_field = 'cancel'
status.boolean = True


class WeekdayListFilter(admin.SimpleListFilter):

    title = _('Day')
    parameter_name = 'day'

    def lookups(self, request, model_admin):
        return [
            (2, 'maandag'),
            (3, 'dinsdag'),
            (4, 'woensdag'),
            (5, 'donderdag'),
            (6, 'vrijdag'),
            (7, 'zaterdag'),
            (1, 'zondag'),
        ]

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(start__week_day=self.value)
        return queryset


class MessageListFilter(admin.SimpleListFilter):

    title = _('notificatie')
    parameter_name = 'notification'
    HAS_MESSAGE = u'1'
    NO_MESSAGE = u'0'

    def lookups(self, request, model_admin):
        return [
            (self.HAS_MESSAGE, 'Heeft notificatie'),
            (self.NO_MESSAGE, 'Geen notificatie'),
        ]

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == self.HAS_MESSAGE:
                queryset = queryset.exclude(message='')
            if self.value() == self.NO_MESSAGE:
                queryset = queryset.filter(message='')
        return queryset


class SessionAdmin(admin.ModelAdmin):
    form = SessionAdminForm
    list_display = [
        session_title,
        'discipline',
        'location',
        'trainer',
        'message',
        status,
        ]
    date_hierarchy = 'start'
    search_fields = ['discipline', 'location', 'trainer', 'description']
    list_filter = [
        #'start', 
        # Add a list filter for future and past.
        WeekdayListFilter,
        'discipline',
        'location',
        'trainer',
        MessageListFilter,
        'cancel',
        'participants',
    ]
    actions = [
        remove,
        duplicate,
        duplicate12,
        go_on,
    ]
    #filter_horizontal = ['participants',]
    # prepopulated_fields = { 'slug': ('discipline', 'location') }
    order_by = ["start"]
    fieldsets = (
        (None, {
            'fields': (
                'start',
                'discipline',
                'location',
                'trainer',
                'participants',
                ),
            }
        ),
        ('Notificatie en afgelasten', {
            'classes': ('collapse',),
            'fields': (
                'message',
                'cancel',
                ),
            }
        ),
    )

admin.site.register(Session, SessionAdmin)
