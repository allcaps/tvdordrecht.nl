# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, HTML, Div

from .admin import AdminImageWidget
from .models import (
    News,
    Image,
)


# class NewsForm(forms.ModelForm):
#
#     class Meta:
#         model = News
#         fields = ['title', 'text']
#
#     def __init__(self, *args, **kwargs):
#         super(NewsForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_tag = False
#         self.helper.layout = Layout(
#             'title',
#             'text',
#             'image',
#         )


class ImageForm(forms.ModelForm):

    image = forms.ImageField(widget=AdminImageWidget)

    class Meta:
        model = Image
        fields = ['image', ]

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'image',
        )


ImageFormSet = inlineformset_factory(
    Image, News, extra=0, min_num=1, can_delete=False, fields=('title', 'text')
)

from django.contrib.auth.models import User


class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['password'].widget = forms.widgets.PasswordInput()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("Dit e-mailadres is al in gebruik. Kies een andere."))
        return self.cleaned_data['email']

    def clean_username(self):
        if User.objects.filter(username__iexact=self.cleaned_data['username']):
            raise forms.ValidationError(_("Deze gebruikersnaam is al in gebruik. Kies een andere."))
        return self.cleaned_data['username']
