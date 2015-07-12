import csv
import datetime

from django.contrib import admin
from django import forms
from django.forms.widgets import TimeInput
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import patterns
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


from .models import (
    SwimTest, 
    Record,
    )

from .forms import UploadCSVFileForm


class HTML5TimeInputWidget(TimeInput):
    input_type = 'time'


class RecordAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RecordAdminForm, self).__init__(*args, **kwargs)
        # Set the default value to '00:00:00'.
        attributes = {'step': '1', 'value': '00:00:00', 'class': 'sTimeField'}
        for field in [
                'time_100',
                'time_200',
                'time_300',
                'time_400',
                'time_500',
                ]:
            self.fields[field].widget = HTML5TimeInputWidget(attrs=attributes)
        # Make pacetime show seconds and readonly.
        self.fields['pace_time'].widget = \
            HTML5TimeInputWidget(attrs={'step': '1'})
        self.fields['pace_time'].widget.attrs['readonly'] = True

    class Meta:
        model = Record
        # exclude = []
        fields = [
            'swim_test',
            'user',
            'time_100',
            'time_200',
            'time_300',
            'time_400',
            'time_500',
            'pace_time',
        ]


class RecordInline(admin.TabularInline):
    model = Record
    form = RecordAdminForm
    extra = 0


class SwimTestAdmin(admin.ModelAdmin):
    inlines = [
        RecordInline,
    ]
    date_hierarchy = 'date'
    list_filter = ['date',]

    class Media:
        css = {"all": ('/static/swimtest/admin/zwemtest.css',)}
        js = ('/static/swimtest/admin/event.js',)

    def get_urls(self):
        urls = super(SwimTestAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^(?P<pk>[0-9]+)/import/$',
                self.admin_site.admin_view(self.import_csv_view))
        )
        return my_urls + urls

    def strptime(self, value, format='%H:%M:%S'):
        return datetime.datetime.strptime(value, format).time()

    def import_csv_view(self, request, pk=None):
        swim_test = get_object_or_404(SwimTest, pk=pk)
        if request.method == 'POST':
            form = UploadCSVFileForm(request.POST, request.FILES)
            if form.is_valid():
                csvfile = request.FILES['file']
                dialect = csv.Sniffer().sniff(csvfile.read(1024))
                csvfile.seek(0)
                reader = csv.reader(csvfile, dialect)
                for row in reader:
                    record = Record(
                        user=get_object_or_404(User, username=row[0]),
                        swim_test=swim_test,
                        time_100=self.strptime(row[2]),
                        time_200=self.strptime(row[4]),
                        time_300=self.strptime(row[6]),
                        time_400=self.strptime(row[8]),
                        time_500=self.strptime(row[10]),
                    )
                    record.save()
                return HttpResponseRedirect('/admin/swimtest/swimtest/%s/' % pk)
        else:
            form = UploadCSVFileForm()
        return render_to_response(
            'swimtest/import_csv.html',
            RequestContext(request, {'form': form}),
        )

admin.site.register(SwimTest, SwimTestAdmin)


class SwimTestYearListFilter(admin.SimpleListFilter):

    title = _('Year')
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        items = []
        date_list = SwimTest.objects.all().dates('date', 'year')
        for years in date_list:
            items.append((years.year, years.year))
        return items

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(swim_test__date__year=self.value)
        return queryset


class RecordAdmin(admin.ModelAdmin):
    # form = RecordAdminForm
    list_display = [
        'swim_test',
        'user',
        'time_100',
        'time_200',
        'time_300',
        'time_400',
        'time_500',
        'display_pace_time',
        'remarks',
    ]
    list_editable = [
        'user',
        'time_100',
        'time_200',
        'time_300',
        'time_400',
        'time_500',
    ]
    list_filter = [
        'swim_test__date',
        SwimTestYearListFilter,
        'user',
    ]
    order_by = ['pace_time']
    readonly_fields = [
        'pace_time'
    ]
admin.site.register(Record, RecordAdmin)
