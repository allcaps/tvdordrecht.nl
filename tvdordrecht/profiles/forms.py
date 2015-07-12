# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Fieldset,
    Layout,
    Div,
    Submit,
)
from crispy_forms.bootstrap import StrictButton

from .models import Profile

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ['user',]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout.append(
            Div (
                StrictButton(
                    'Save',
                    css_class='btn-primary',
                    type='submit'
                ),
            )

        )