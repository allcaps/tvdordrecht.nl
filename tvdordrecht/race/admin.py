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
    list_display = ['name', 'city', 'website']
    list_filter = ['city', ]
    inlines = [ResultInline, ]
    prepopulated_fields = {'slug': ('name', 'city'), }
    fieldsets = (
        (None, {
            'classes': ('wide', 'extrapretty'),
            'fields': ('name', 'city', 'website', 'text')
        }),

        ('Geavanceerde opties', { #Geavanceerde opties
            'classes': ('collapse', 'wide', 'extrapretty'),
            'fields': ('image', 'slug')
        }),
    )

    class Media:
        js = ckeditor

admin.site.register(Event, EventAdmin)


class DistanceAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'name', 'order', 'default']
    list_editable = ['name', 'order', 'default']
    actions = ['delete_selected', ]

admin.site.register(Distance, DistanceAdmin)


class ResultAdmin(admin.ModelAdmin):
    list_display = ['event', 'date', 'user', 'time', 'remarks']
    list_filter = ['distance', 'user']
    pass

admin.site.register(Result, ResultAdmin)
