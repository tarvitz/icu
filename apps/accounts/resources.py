from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication
from tastypie import fields
from tastypie.throttle import BaseThrottle, CacheThrottle 
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

from django.conf import settings

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get']
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser', 'phone', ]
        fields = ('id', 'username', 'date_joined',
            'first_name', 'last_name',
        )
        authorization = Authorization()
        authentication = ApiKeyAuthentication()
        throttle = BaseThrottle()
        if settings.ENABLE_THROTTLING:
            throttle = CacheThrottle(throttle_at=settings.THROTTLE_AT)
        filtering = {
            'username': ALL,
        }
