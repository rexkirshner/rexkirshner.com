from django.conf.urls import patterns, include, url


urlpatterns = patterns('map.views',
    url(r'$', 'location_history'),
)