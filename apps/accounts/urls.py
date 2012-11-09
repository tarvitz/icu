from django.conf.urls import patterns, include, url
from apps.core.shortcuts import direct_to_template

urlpatterns = patterns('apps.accounts.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^profile/$', 'profile', name='profile'),
    url(r'^register/$', 'register', name='register'),
    url(r'^invite/$', 'invite', name='invite'),
    url(r'^invite/register/success/$', direct_to_template,
        {'template': 'accounts/invite_register_success.html'},
        name='invite-register-success'),
    url(r'^invite/success/$', direct_to_template,
        {'template': 'accounts/invite_success.html'},
        name='invite-success'),
    url(r'^invite/register/(?P<sid>[\w\d]+)/$',
        'invite_register', name='invite-register'),
    url(r'^xhr/reload/api/key/$',
        'generate_new_api_key', name='reload-api-key'),
)
