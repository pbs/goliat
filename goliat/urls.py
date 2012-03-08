from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url('^about/', include('goliat.about.urls')),
    url('^', include('goliat.explorer.urls')),
)

urlpatterns += staticfiles_urlpatterns()
