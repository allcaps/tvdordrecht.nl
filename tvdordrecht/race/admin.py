# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import (
    Event,
    Distance,
    Result,
)


class ResultInline(admin.TabularInline):
    model = Result
    extra = 0


class ResultInline(admin.TabularInline):
    model = Result
    extra = 0


class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'website']
    list_filter = ['city', ]
    inlines = [ResultInline, ]
    prepopulated_fields = {'slug': ('name', 'city'), }

admin.site.register(Event, EventAdmin)


class DistanceAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'name', 'order', 'default']
    list_editable = ['name', 'order', 'default']
    actions = ['delete_selected', ]

admin.site.register(Distance, DistanceAdmin)


class ResultAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'edition', 'user', 'time', 'remarks']
    list_filter = ['race__distance', 'user']
    pass

admin.site.register(Result, ResultAdmin)
