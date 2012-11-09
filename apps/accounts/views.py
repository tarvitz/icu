# Create your views here.
# -*- coding: utf-8 -*-
from apps.core.helpers import render_to, ajax_response, get_object_or_None
from apps.core.decorators import lock, login_required_json
from apps.accounts.models import Invite
from apps.accounts.decorators import check_invite
from apps.accounts.forms import (
    LoginForm, AccountRegisterForm, SendInviteForm, InviteRegisterForm
)

from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import transaction
from django.utils.translation import ugettext_lazy as _


@render_to('accounts/login.html')
def login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.cleaned_data['user']
            auth.login(request, user)
            return {'redirect': 'core:index'}
    return {
        'form': form
    }


@render_to('index.html')
def logout(request):
    auth.logout(request)
    return {}


@render_to('accounts/profile.html')
def profile(request):
    return {}


@login_required_json
@ajax_response
def generate_new_api_key(request):
    if request.method == 'POST':
        request.user.api_key.key = request.user.api_key.generate_key()
        request.user.api_key.save()
        key = request.user.api_key.key
        return {'success': True, 'key': key}
    return {'success': False}


@lock("REGISTER_ALLOWED")
@render_to('accounts/register.html')
def register(request):
    form = AccountRegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return {'redirect': 'core:index'}
    return {
        'form': form
    }


@login_required
@render_to('accounts/invite.html')
def invite(request):
    form = SendInviteForm(request.POST or None, request=request)
    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=False)
            invite = form.instance
            email = form.cleaned_data['email']
            msg = settings.INVITE_MESSAGE % {
                'user': request.user.username,
                'link': "http://b3ban.blacklibrary.ru%s" % reverse('accounts:invite-register', args=(invite.sid, ))
            }
            #no mail send, no money :)
            send_mail(
                subject=unicode(_('You have been invited to b3ban service')),
                message=unicode(msg),
                from_email=settings.EMAIL_FROM,
                recipient_list=[email]
            )
            invite.save()
            return {'redirect': 'accounts:invite-success'}
    return {
        'form': form
    }


#@check for possibility to register
@transaction.commit_on_success
@check_invite(sid='sid')
@render_to('accounts/invite_register.html')
def invite_register(request, sid):
    invite = get_object_or_None(Invite, sid=sid)
    if not invite:
        return {'redirect': 'core:ufo'}
    form = InviteRegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            invite.is_verified = True
            invite.save()
            user = form.save(commit=False)
            user.email = invite.email
            user.set_password(form.cleaned_data['password'])
            user.save()
            return {'redirect': 'accounts:invite-register-success'}
    return {'form': form, 'sid': sid}
