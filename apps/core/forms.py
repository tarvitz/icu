# coding: utf-8
#
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.util import ErrorList
from apps.core.helpers import get_object_or_None


class RequestModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs['request']
            del kwargs['request']
        super(RequestModelForm, self).__init__(*args, **kwargs)

