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


# class EditionForm(forms.ModelForm):
#     distances = forms.ModelMultipleChoiceField(
#         queryset=Distance.objects.all(),
#         label='Wedstrijden',
#         help_text="Selecteer alle wedstrijden die georganiseerd worden.",
#         required=True,
#         widget=forms.CheckboxSelectMultiple(),
#     )
#
#     class Meta:
#         model = Edition
#         exclude = []
#
#     def __init__(self, *args, **kwargs):
#         super(EditionForm, self).__init__(*args, **kwargs)
#         self.fields['event'].widget = forms.HiddenInput()
#         self.fields['date'].label = "Editie (datum)"
#         self.fields['date'].help_text = "Bijvoorbeeld: 29-08-2015"
#
#     def save(self, commit=True):
#         """
#         This save method only allows adding new races, but not removing them.
#         """
#         edition = super(EditionForm, self).save()
#         for distance in self.cleaned_data['distances']:
#             Race.objects.get_or_create(edition=edition, distance=distance)


# class RaceForm(forms.ModelForm):
#     class Meta:
#         model = Race
#         exclude = []


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['slug', 'image', 'pub_date']

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['website'].help_text = None


# class ResultForm(forms.ModelForm):
#     class Meta:
#         model = Result
#         exclude = []


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


# class WhoWhatWhereEditionForm(forms.Form):
#     edition = forms.ModelChoiceField(
#         queryset=Edition.objects.all(),
#         label='Editie',
#         required=True,
#         empty_label=None,
#         widget=forms.widgets.RadioSelect(),
#     )


# class WhoWhatWhereRaceForm(forms.Form):
#     race = forms.ModelMultipleChoiceField(
#         queryset=Race.objects.all(),
#         label='Aan welke wedstrijd ga je deelnemen?',
#         required=True,
#         widget=forms.CheckboxSelectMultiple(),
#     )


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

class ResultForm0(forms.Form):
    result = forms.ChoiceField(
        label='Wedstrijd',
        required=True,
        widget=forms.widgets.RadioSelect()
    )

class ResultForm1(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['time', 'remarks']
