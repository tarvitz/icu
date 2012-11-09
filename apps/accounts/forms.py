# -*- coding: utf-8 -*-
from django import forms
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _

from django.contrib import auth
from django.contrib.auth.models import User
from django.conf import settings

from apps.core.helpers import get_object_or_None
from apps.core.forms import RequestModelForm
from apps.accounts.models import Invite

from uuid import uuid1


class LoginForm(forms.Form):
    username = forms.CharField(label=_("Username"))
    password = forms.CharField(
        label=_("Password"), widget=forms.PasswordInput())

    def clean(self):
        cd = self.cleaned_data
        username = cd.get('username')
        password = cd.get('password')
        user = auth.authenticate(username=username, password=password)

        if not user:
            # fail to authenticate, probabbly incorrect auth data
            msg = _("Sorry your username or/and password are invalid")
            self._errors['password'] = ErrorList([msg])
            if 'password' in cd:
                del cd['password']

        cd['user'] = user
        return cd


class AccountRegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        required=True, label=_("Repeat password"),
        help_text=_("Repeat password"),
        widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        user = get_object_or_None(User, username__iexact=username)
        if user:
            raise forms.ValidationError(
                _("Sorry but such username already taken, \
                  please choose another or login"))
        return username

    def clean(self):
        cd = self.cleaned_data
        password = cd.get('password') or None
        password2 = cd.get('password2') or None

        if all((password, password2)):
            if password != password2:
                msg = _("Passwords does not match, please correct them")
                self._errors['password'] = ErrorList([msg])
                if 'password' in cd:
                    del cd['password']
        return cd

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        widgets = {
            'password': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

class InviteRegisterForm(AccountRegisterForm):
    password = forms.CharField(
        label=_("Password"), required=True,
        widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', )

class SendInviteForm(RequestModelForm):
    def clean(self):
        cd = self.cleaned_data
        user = self.request.user
        if user.invites >= settings.MAX_INVITES_COUNT:
            msg = _("Your are out of invite limit, sorry for that :)")
            self._errors['email'] = ErrorList([msg])
            if 'email' in cd:
                del cd['email']
        return cd

    def save(self, commit=True):
        super(SendInviteForm, self).save(commit=commit)
        self.instance.sid = uuid1().get_hex()
        self.instance.sender = self.request.user

    class Meta:
        model = Invite
        fields = ('email', )
