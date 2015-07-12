# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Div,
)
from crispy_forms.bootstrap import StrictButton


class SwimTestSearchForm(forms.Form):
    """ Form to search `SwimTest` objects. """

    def __init__(self, *args, **kwargs):
        super(SwimTestSearchForm, self).__init__(*args, **kwargs)
        self.fields['user'] = forms.ModelChoiceField(
            queryset=User.objects.all(),
            label='Deelnemer',
            required=False,
            empty_label="Alle deelnemers",
        )
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'form-inline hidden-print'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
            Div(
                'user',
                StrictButton(
                    '<span class="glyphicon glyphicon-search"></span>',
                    css_class='btn-primary',
                    type='submit'
                ),
            )
        )


class UploadCSVFileForm(forms.Form):
    """ Form to upload a CSV file.
    """
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(UploadCSVFileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-inline hidden-print'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
            Div (
                'file',
                StrictButton(
                    'Importeer',
                    css_class='btn-primary',
                    type='submit'
                ),
            )
        )