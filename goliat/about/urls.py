from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
        url('^$', 'django.views.generic.simple.direct_to_template', {
            'template': 'about/index.html'
        }, 'about'),
)
