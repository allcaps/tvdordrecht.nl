# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Menu, Image, Page, News

from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.conf import settings
import os, sys, glob

from datetime import datetime
from time import sleep


ckeditor = ['/static/webapp/ckeditor/ckeditor.js','/static/webapp/ckeditor.init.js']
ckeditor_css = ['/static/webapp/webapp.css']


def remove(modeladmin, request, queryset):
    queryset.delete()
remove.short_description = "Verwijderen"


def make_published(modeladmin, request, queryset):
    queryset.update(publish=True)
make_published.short_description = "Zet publiceren aan"


def make_depublished(modeladmin, request, queryset):
    queryset.update(publish=False)
make_depublished.short_description = "Zet publiceren uit"


def clear_thumbnails(modeladmin, request, queryset):
    for i in queryset:
        root = settings.MEDIA_ROOT
        file_name = i.image
        basedir = os.path.dirname("%s%s" %(root, file_name))
        base, ext = os.path.splitext(os.path.basename(str(file_name)))
        for file in glob.glob(r"%s/%s_[c|t]_*x*%s" %(basedir, base, ext)):
            os.remove(file)     
clear_thumbnails.short_description = "Delete thumnails"


def refresh_thumbnails(modeladmin, request, queryset):
    for obj in queryset:
        root = settings.MEDIA_ROOT
        file_name = obj.image
        basedir = os.path.dirname("%s%s" %(root, file_name))
        base, ext = os.path.splitext(os.path.basename(str(file_name)))
        for file in glob.glob(r"%s/%s_[c|t]_*x*%s" %(basedir, base, ext)):
            os.remove(file)  
        obj.save()
        sleep(2)
refresh_thumbnails.short_description = "Refresh thumnails"


class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'sortorder', 'last_modified', 'last_modified_by', 'keywords', 'description']
    #list_filter = ['', ]
    ordering = ['sortorder',]
    prepopulated_fields = { 'slug': ('title', ) }
    actions = None
    list_editable = ['sortorder',]
    fieldsets = (
        (None, {
            'classes': ('wide', 'extrapretty'),
            'fields': ('title', 'text')
        }),

        ('Geavanceerde opties', { #Geavanceerde opties
            'classes': ('collapse', 'wide', 'extrapretty'),
            'fields': ('image', 'slug', 'sortorder')
        }),

        ('Meta tags', {
            'classes': ('collapse', 'wide', 'extrapretty'),
            'fields': ('description', 'keywords', )
        }),
    )

    class Media:
        js = ckeditor
        
        
admin.site.register(Menu, MenuAdmin)


def thumbnail(file_path):
    path, ext = file_path.rsplit('.', 1)
    return u'<img src="%s_t_132x132.%s?now=%s" />' % (path, ext, datetime.now().isoformat())


class AdminImageWidget(AdminFileWidget):
    """
    A FileField Widget that displays an image instead of a file path
    if the current file is an image.
    """
    def render(self, name, value, attrs=None):
        output = []
        if value:
            file_path = '%s%s' % (settings.MEDIA_URL, value)
            try:
                output.append('<a target="_blank" href="%s?now=%s">%s</a><br />' %
                        (file_path, datetime.now().isoformat(), thumbnail(file_path)))
            except IOError:
                output.append('%s <a target="_blank" href="%s">%s</a> <br />%s ' %
                        ('Currently:', file_path, value, 'Change:'))

        output.append(super(AdminImageWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class ImageUploadForm(forms.ModelForm):
    image = forms.ImageField(widget=AdminImageWidget)

    class Meta:
        model = Image
        exclude = []


class ImageAdmin(admin.ModelAdmin):
    form = ImageUploadForm
    search_fields = ['image', ]
    list_display = ['filename', 'list_thumbnail', 'image_editing', 'inline_urls', 'pub_date', 'last_modified', 'owner','last_modified_by'] #sort_order #'inline_urls',
    # list_display = ['filename', 'image',]
    list_editable = ['image_editing', ]
    list_per_page = 50
    date_hierarchy = 'pub_date'
    actions = [remove, clear_thumbnails, refresh_thumbnails]
    #list_filter = ['type',]
    fieldsets = (
        (None, {
            'fields': ('image', ),
            'classes': ['wide', 'extrapretty']
        }),
        ('Geavanceerde opties', {
            'classes': ('collapse', 'wide', 'extrapretty',),
            'fields': ('caption', 'image_editing') #'sortorder',
        }),
    )
admin.site.register(Image, ImageAdmin)


class PageAdmin(admin.ModelAdmin):
    """
    # ['html', 'id', 'intro', 'keywords', 'last_modified', 'last_modified_by_id', 'menu_id', 'owner_id', 'pub_date', 'publish', 'slideshow_id', 'slug', 'sortorder', 'table_of_contents', 'text', 'title']
    """
    search_fields = ['title', 'text']
    list_display = ['title', 'publish', 'menu', 'sortorder', 'pub_date', 'last_modified', 'owner','last_modified_by', 'keywords', 'description']
    list_filter = ['menu', 'publish']
    list_editable = ['menu', 'publish', 'sortorder']
    prepopulated_fields = {'slug': ('title', )}
    actions = [remove, make_published, make_depublished]
    fieldsets = (
        (None, {
            'classes': ('wide', 'extrapretty'),
            'fields': ('menu', 'title', 'image')
        }),
        (None, {
            'classes': ('wide', 'extrapretty'),
            'fields': ('text', )
        }),
        ('Geavanceerde opties', {
            'classes': ('collapse', 'wide', 'extrapretty'),
            'fields': ('publish', 'slug', 'sortorder')
        }),
        ('Meta tags', {
            'classes': ('collapse', 'wide', 'extrapretty'),
            'fields': ('description', 'keywords')
        }),
    )

    class Media:
        js = ckeditor

admin.site.register(Page, PageAdmin)


class NewsAdmin(admin.ModelAdmin):
    """
        'id', 'publish', 'title', 'slug', 'text', 'location_id', 'general', 
        'owner_id', 'pub_date', 'last_modified_by_id', 'last_modified'
    """
    list_display = ['title', 'publish', 'pub_date', 'last_modified', 'owner', 'last_modified_by']
    list_filter = ['owner', ]
    actions = [remove, make_published, make_depublished]
    search_fields = ['title', 'text', ]
    prepopulated_fields = { 'slug': ('title', ) }
    #filter_horizontal = ['image', ]
    date_hierarchy = 'pub_date'
 
    fieldsets = (
        (None, {
            'classes': ['wide', 'extrapretty'],
            'fields': ('title', 'image', 'text')
        }),
        ('Geavanceerde opties', {
            'classes': ('collapse', 'wide', 'extrapretty'),
            'fields': ('publish', 'slug', 'pub_date')
        }),
        ('Meta tags', {
            'classes': ('collapse', 'wide', 'extrapretty'),
            'fields': ('description', 'keywords')
        }),
    )
       
    class Media:
        js = ckeditor

admin.site.register(News, NewsAdmin)


# class SponsorAdmin(admin.ModelAdmin):
#     """
#     The model has more fields than utilised for future feat.
#     """
#     search_fields = ['name', 'url', 'text']
#     list_display = ['name', 'publish', 'sortorder', 'pub_date', 'last_modified', 'owner','last_modified_by']
#     list_filter = ['publish', ]
#     list_editable = ['publish', 'sortorder', ] #'menu'
#     prepopulated_fields = { 'slug': ('name', ) }
#     actions = [remove, make_published, make_depublished]
#     #filter_horizontal = ['images', ]
#
#     fieldsets = (
#             (None, {
#                 'classes': ('wide', 'extrapretty'),
#                 'fields': ('name', 'image', 'url')
#             }),
#
#             ('Geavanceerde opties', {
#                 'classes': ('collapse', 'wide', 'extrapretty'),
#                 'fields': ('publish', 'slug', 'sortorder')
#             }),
#
#             ('Meta tags', {
#                 'classes': ('collapse', 'wide', 'extrapretty'),
#                 'fields': ('description', 'keywords', )
#             }),
#         )
#
# admin.site.register(Sponsor, SponsorAdmin)
