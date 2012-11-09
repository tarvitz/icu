# -*- coding: utf-8 -*-
from django import forms
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _

from apps.banlist.models import BanList, UserBanList, ServerBanList


class AddServerBanForm(forms.ModelForm):
    class Meta:
        model = ServerBanList
        fields = ('server_name', 'plain_type', 'ip_address', 'reason')
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 5})
        }
        exclude = ['owner', ]
