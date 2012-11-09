from django.conf.urls.defaults import patterns, include, url
from apps.core.shortcuts import direct_to_template


urlpatterns = patterns('apps.core.views',
    url(r'^$', 'index', name='index'),
    #static
    url(r'^function/blocked/$', direct_to_template,
        {'template': 'static/function_blocked.html'},
        name='blockage'),
    url(r'^ufo/$', direct_to_template,
        {'template': 'static/ufo.html'},
        name='ufo'),
)
