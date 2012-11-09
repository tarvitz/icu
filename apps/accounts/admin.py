#coding: utf-8
from django import forms
from django.db import models
from django.db.models import Q,F
from django.contrib import admin
from apps.accounts.models import Invite
from django.utils.translation import ugettext_lazy as _

class InviteAdmin(admin.ModelAdmin):
    list_display = ('sender', 'email', 'is_verified', 'created_on')
admin.site.register(Invite, InviteAdmin)
