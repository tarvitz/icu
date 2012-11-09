# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from datetime import datetime, timedelta
# your models here


class Invite(models.Model):
    is_expired = models.BooleanField(
        _("is expired?"), default=False)
    expire_date = models.DateTimeField(
        _("expire date"), help_text=_("date and time when invite is expired"),
        default=datetime.now() + timedelta(days=7)
    )
    created_on = models.DateTimeField(
        _("created on"), help_text=_("created date of invitation"),
        default=datetime.now, auto_now_add=True
    )
    updated_on = models.DateTimeField(
        _("updated on"), help_text=_("date when this was updated last time"),
        default=datetime.now, auto_now=True
    )
    sender = models.ForeignKey(
        User,
        related_name='invite_sender_user_set', null=True
    )
    email = models.EmailField(
        _("Email"), help_text=_("Friend email"), null=True,
        unique=True
    )
    sid = models.CharField(
        _("SID"), help_text=_("SpecialID for registration"),
        max_length=128
    )
    is_verified = models.BooleanField(
        _("is verified?"), help_text=_("shows if user is verified"),
        default=False)

    def __unicode__(self):
        return "%s [%s]" % (self.sender.username, self.email)

    class Meta:
        verbose_name = _("Invite")
        verbose_name_plural = _("Invites")
        ordering = ['-created_on', '-updated_on']


User.add_to_class(
    'invites', models.PositiveSmallIntegerField(
        _('invites'), help_text=_("intites count"), default=0)
)


class UserExtenssion(object):
    """ overrides, extenssions and so on """
    pass

User.__bases__ = (UserExtenssion,) + User.__bases__

from django.contrib.auth.admin import UserAdmin
UserAdmin.list_display += ('invites', )
#UserAdmin.fieldsets += ((
#    _('Profile'),
#    {
#        'fields': ('invites', ),
#        'classes': ('collapse',),
#    }
#),)


# signals
from apps.accounts.signals import setup_signals
setup_signals()
