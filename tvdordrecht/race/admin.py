# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import (
    Event,
    Distance,
    Result,
)

ckeditor = ['/static/webapp/ckeditor/ckeditor.js','/static/webapp/ckeditor.init.js']


class ResultInline(admin.TabularInline):
    model = Result
    extra = 0
    fields = ['user', 'date', 'distance', 'time', 'remarks']


class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'website',
                    'owner', 'pub_date', 'last_modified_by', 'last_modified']
    list_filter = ['city', ]
    inlines = [ResultInline, ]
    prepopulated_fields = {'slug': ('name', 'city'), }
    fieldsets = (
        (None, {
            'classes': ('wide', 'extrapretty'),
            'fields': ('name', 'city', 'website', 'text')
        }),

        ('Geavanceerde opties', {
            'classes': ('collapse', 'wide', 'extrapretty'),
            'fields': ('image', 'slug')
        }),
    )

    class Media:
        js = ckeditor

admin.site.register(Event, EventAdmin)


class DistanceAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'name', 'order',
                    'owner', 'pub_date', 'last_modified_by', 'last_modified']
    list_editable = ['name', 'order']
    actions = ['delete_selected', ]

admin.site.register(Distance, DistanceAdmin)


class ResultAdmin(admin.ModelAdmin):
    list_display = ['event', 'date', 'distance', 'user', 'time', 'remarks',
                    'owner', 'pub_date', 'last_modified_by', 'last_modified']
    list_filter = ['event', 'distance', 'user', 'time']
    list_editable = ['time',]
    date_hierarchy = 'date'

admin.site.register(Result, ResultAdmin)
