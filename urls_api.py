from django.conf.urls.defaults import patterns, url, include
from apps.accounts.resources import UserResource
from apps.banlist.resources import ServerBanListResource
from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(ServerBanListResource())
v1_api.register(UserResource())

urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),
)
