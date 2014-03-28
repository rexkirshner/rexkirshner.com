from django.conf.urls import patterns, include, url


urlpatterns = patterns('map.views',
    url(r'api/location_history.kml$', 'location_history'),

    url(r'$', 'index'),
    
)