from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.banlist.views',
    url(r'^$', 'index', name='index'),
    url(r'^add/$', 'add', name='add'),
    url(r'^edit/(?P<pk>\d+)/$', 'edit', name='edit'),
    url(r'^delete/(?P<pk>\d+)/$', 'delete', name='delete'),
)
