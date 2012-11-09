from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class BanList(models.Model):
    plain_type = models.CharField(
        _("Type"),
        max_length=64,
        help_text=_("Ban type, e.x. can not \
                    login beacuse of being banned as RUSSIAN"),
        default='default'
    )
    reason = models.CharField(
        _('reason'), blank=True, null=True,
        max_length=4096
    )
    created_on = models.DateTimeField(
        _('created on'), auto_now_add=datetime.now)
    updated_on = models.DateTimeField(
        _('updated on'), auto_now=datetime.now
    )
    owner = models.ForeignKey(User)

    class Meta:
        abstract = True


class UserBanList(BanList):
    nickname = models.CharField(
        _("Nickname"), help_text=_("Nickname of banned user"),
        max_length=512,
    )

    class Meta:
        ordering = ['created_on', ]


class ServerBanList(BanList):
    ip_address = models.IPAddressField(
        _('ip address'), help_text=_("Server ip address"))
    server_name = models.CharField(
        _('server name'), max_length=512, blank=True, null=True)

    class Meta:
        ordering = ['created_on', ]
