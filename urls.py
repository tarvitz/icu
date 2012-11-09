from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'template.views.home', name='home'),
    # url(r'^template/', include('template.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'grappelli/', include('grappelli.urls')),
    url(r'admin/', include(admin.site.urls)),
    url(r'^', include('apps.core.urls', namespace='core')),
    url(r'^', include('apps.accounts.urls', namespace='accounts')),
    url(r'^banlist/', include('apps.banlist.urls', namespace='banlist')),
    url(r'', include('urls_api')),

)
