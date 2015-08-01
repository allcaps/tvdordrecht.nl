# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Field,
    Div,
)
from crispy_forms.bootstrap import (
    StrictButton,
)

from .models import (
    Event,
    Distance,
    Result,
)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['slug', 'image', 'pub_date']

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['website'].help_text = None


class WhoWhatWhereEventForm(forms.Form):
    event = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        label='Evenement',
        required=True,
        empty_label=None,
        widget=forms.widgets.RadioSelect(),
    )

    def __init__(self, *args, **kwargs):
        super(WhoWhatWhereEventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'event',
        )


class WhoWhatWhereDetailForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(WhoWhatWhereDetailForm, self).__init__(*args, **kwargs)
        self.fields['distance'].widget = forms.widgets.RadioSelect()
        self.fields['distance'].empty_label = None

    class Meta:
        model = Result
        exclude = ['event', 'pub_date', 'time', 'remarks']


class ResultForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ResultForm, self).__init__(*args, **kwargs)
        self.fields['time'].required = True

    class Meta:
        model = Result
        fields = ['time', 'remarks']


class EditionSearchForm(forms.Form):
    """ Form to search `Edition` objects. """
    q = forms.CharField(label='', required=False)

    def __init__(self, *args, **kwargs):
        super(EditionSearchForm, self).__init__(*args, **kwargs)
        self.fields['user'] = forms.ModelChoiceField(
            queryset=User.objects.all(),
            label='Deelnemer',
            required=False,
            empty_label="Alle deelnemers"
        )
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'form-inline hidden-print'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
            Div(
                Field('q', placeholder="Search"),
                'user',
                StrictButton(
                    '<span class="glyphicon glyphicon-search"></span>',
                    css_class='btn-primary',
                    type='submit'
                ),
            )
        )
