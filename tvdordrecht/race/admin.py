# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import (
    Event,
    Edition,
    Distance,
    Race,
    Result,
)


class EditionInline(admin.TabularInline):
    model = Edition
    extra = 0


class ResultInline(admin.TabularInline):
    model = Result
    extra = 0


class RaceInline(admin.TabularInline):
    model = Race
    extra = 0


class ResultInline(admin.TabularInline):
    model = Result
    extra = 0


class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'website']
    list_filter = ['city', ]
    inlines = [EditionInline, ]
    prepopulated_fields = {'slug': ('name', 'city'), }

admin.site.register(Event, EventAdmin)


class EditionAdmin(admin.ModelAdmin):
    list_display = ['date', 'event']
    list_filter = ['date', 'event__name', 'event__city']
    search_fields = ['event__name', 'event__city']
    date_hierarchy = 'date'
    inlines = [RaceInline, ]

admin.site.register(Edition, EditionAdmin)


class DistanceAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'name', 'order', 'default']
    list_editable = ['name', 'order', 'default']
    actions = ['delete_selected', ]

admin.site.register(Distance, DistanceAdmin)


class RaceAdmin(admin.ModelAdmin):
    list_display = ['distance', 'edition']
    list_filter = ['distance', 'edition', 'edition__event']
    inlines = [ResultInline, ]
admin.site.register(Race, RaceAdmin)


class ResultAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'edition', 'user', 'time', 'remarks']
    list_filter = ['race__distance', 'user']
    pass

admin.site.register(Result, ResultAdmin)
