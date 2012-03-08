from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('goliat',
    url('^$', 'explorer.views.landing'),
    url('^source/(.+)/$', 'explorer.views.source'),
    # This one is very generic, keep it as down as possible
    url('^(.+)/$', 'explorer.views.result'),
)
