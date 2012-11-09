#coding: utf-8
from django import forms
from django.db import models
from django.db.models import Q,F
from django.contrib import admin
from apps.banlist.models import UserBanList, ServerBanList
from django.utils.translation import ugettext_lazy as _

class UserBanListAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'created_on')
admin.site.register(UserBanList, UserBanListAdmin)

class ServerBanListAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'server_name', 'created_on')

admin.site.register(ServerBanList, ServerBanListAdmin)
