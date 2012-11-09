import re
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from apps.banlist.models import ServerBanList
from tastypie.authorization import Authorization
from tastypie.throttle import BaseThrottle, CacheThrottle
from tastypie.authentication import ApiKeyAuthentication
from tastypie.validation import Validation, FormValidation
from tastypie import fields

from apps.accounts.resources import UserResource
from django.db.models import Q, F
from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.util import ErrorList

from django.conf.urls.defaults import url
from tastypie.http import HttpGone, HttpMultipleChoices
from tastypie.utils import trailing_slash
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ImproperlyConfigured

from apps.core.helpers import get_object_or_404

class ServerBanListResource(ModelResource):
    owner = fields.ForeignKey(UserResource, attribute='owner', readonly=True)
    #read-onlies
    id = fields.IntegerField(readonly=True, attribute='id')
    created_on = fields.DateTimeField(readonly=True, attribute='created_on',
        help_text=_('Shows when spot was created'))
    
    #creates and associates instance.owner with request.user
    def obj_create(self, bundle, request=None, **kwargs):
        return super(ServerBanListResource, self).obj_create(bundle, request,
            owner=request.user)
        
    #retrieve only objects we own or permitted to alter
    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(Q(owner=request.user))

    class Meta:
        queryset = ServerBanList.objects.all()
        allowed_methods = ['get', 'post', 'put', 'patch', 'delete']
        resource_name = 'server'
        authorization = Authorization()
        authentication = ApiKeyAuthentication()
        throttle = BaseThrottle(throttle_at=settings.THROTTLE_AT)
        if settings.ENABLE_THROTTLING:
            throttle = CacheThrottle(throttle_at=settings.THROTTLE_AT)
        #validation = FormValidation(form_class=RepSpotForm)
        filtering = {
            'owner': ALL_WITH_RELATIONS,
            'server_name': ALL,
            'ip_address': ALL,
            'reason': ALL,
            'plain_type': ALL,
        }

