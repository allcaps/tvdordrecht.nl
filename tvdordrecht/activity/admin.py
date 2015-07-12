from datetime import (
    datetime,
    timedelta,
    )

from django import forms
from django.contrib import admin

from .models import (
    Activity,
    Category,
    )


admin.site.disable_action('delete_selected')


def remove(modeladmin, request, queryset):
    queryset.delete()
remove.short_description = "Verwijderen"


def make_published(modeladmin, request, queryset):
    queryset.update(publish=True)
make_published.short_description = "Zet publiceren aan"


def make_depublished(modeladmin, request, queryset):
    queryset.update(publish=False)
make_depublished.short_description = "Zet publiceren uit"


def duplicate(modeladmin, request, queryset):
    """ Duplicate action.
        Duplicates each item in the queryset to the next week.
        Skips to the next week if a similar object already exists.
    """
    for i in queryset:
        created = False
        offset = timedelta()
        while not created:
            offset += timedelta(weeks=1)
            obj, created = Activity.objects.get_or_create(
                category=i.category,
                start_date=i.start_date + offset,
                slug=i.slug)
        # Caluclate the correct end date.
        if i.end_date:
            obj.end_date = i.end_date + offset
        # Set the other fields...
        for attr in ['title', 'publish', 'all_day', 'start_time', 'end_time']:
            setattr(obj, attr, i.__getattribute__(attr))
        obj.save()

duplicate.short_description = "Dupliceer"


def duplicate12(modeladmin, request, queryset):
    """ Duplicate 12 action.
        Duplicates each item in the queryset to the next week.
        Continues duplicating until 12 duplicates are created.
        Skips to the next week if a similar object already exists.
    """
    for i in queryset:
        count = 0
        while count < 12:
            created = False
            offset = timedelta()
            while not created:
                offset += timedelta(weeks=1)
                obj, created = Activity.objects.get_or_create(
                    category=i.category,
                    start_date=i.start_date + offset,
                    slug=i.slug)
            # Caluclate the correct end date.
            if i.end_date:
                obj.end_date = i.end_date + offset
            # Set the other fields...
            for attr in ['title', 'publish', 'all_day', 'start_time',
                    'end_time']:
                setattr(obj, attr, i.__getattribute__(attr))
            obj.save()
            count += 1

duplicate12.short_description = "Dupliceer 12 keer"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', ]
    ordering = ['title', ]
    prepopulated_fields = {'slug': ('title', )}
    actions = None
    fieldsets = (
            (None, {
                'fields': ('title', 'text'),
            }),
            ('Geavanceerde opties', {
                'classes': ('collapse',),
                'fields': ('slug', )
            }),
    )

    class Media:
        js = ['/static/webapp/tiny_mce/tiny_mce.js',
            '/static/webapp/tiny_mce/textareas.js']

admin.site.register(Category, CategoryAdmin)


class ActivityAdminForm(forms.ModelForm):

    class Meta:
        model = Activity
        exclude = []
        # fields = [
        #     'publish',
        #     'category',
        #     'title',
        #     'slug',
        #     'all_day',
        #     'start_date',
        #     'start_time',
        #     'end_date',
        #     'end_time',
        #     'description',
        #     'participants',
        # ]


    def clean(self):
        data = self.cleaned_data
        if data['all_day']:
            # Event spans all day.
            if data['end_date'] and data['start_date'] > data['end_date']:
                raise forms.ValidationError(u"Einddatum voor begindatum.")
        else:
            # Event with start and end time.
            if data['start_time'] is None:
                raise forms.ValidationError(
                    u"Zet All-day aan of vul alle datum- en tijdvelden in." +
                    u"Begintijd ontbreekt.")
            if data['end_date'] is None:
                raise forms.ValidationError(
                    u"Zet All-day aan of vul alle datum- en tijdvelden in. " +
                    u"Einddatum ontbreekt.")
            if data['end_time'] is None:
                raise forms.ValidationError(
                    u"Zet All-day aan of vul alle datum- en tijdvelden in. " +
                    u"Eindtijd ontbreekt.")
            if datetime.combine(data['start_date'], data['start_time']) >= \
                    datetime.combine(data['end_date'], data['end_time']):
                raise forms.ValidationError(u"Eind voor begin.")
        return self.cleaned_data


class ActivityAdmin(admin.ModelAdmin):
    form = ActivityAdminForm
    list_display = [
        'title',
        'category',
        'publish',
        'all_day',
        'start_date',
        'start_time',
        'end_date',
        'end_time',
        #'participants_display_list'
        ]
    date_hierarchy = 'start_date'
    search_fields = ['title', 'description']
    list_filter = ['publish', 'category', 'all_day']
    prepopulated_fields = {'slug': ('title', )}
    filter_horizontal = ['participants', ]
    actions = [
        remove,
        make_published,
        make_depublished,
        duplicate,
        duplicate12,
    ]
    order_by = ["start_date", "start_time"]
    fieldsets = (
        (None, {
            'fields': (
                'category',
                'title',
                'all_day',
                ('start_date', 'start_time'),
                ('end_date', 'end_time'),
                'description',
                ),
            }
        ),
        ('Deelnemers', {
            'classes': ('collapse', ),
            'fields': (
                'participants',
                ),
            }
        ),
        ('Geavanceerde opties', {
            'classes': ('collapse', ),
            'fields': (
                'publish',
                'slug',
                ),
            }
        ),
    )

    class Media:
        js = [
            '/static/webapp/tiny_mce/tiny_mce.js',
            '/static/webapp/tiny_mce/textareas-no-image.js',
        ]

admin.site.register(Activity, ActivityAdmin)
