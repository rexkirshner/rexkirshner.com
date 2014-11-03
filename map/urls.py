from django.conf.urls import patterns, include, url


urlpatterns = patterns('map.views',
    #url(r'api/location_history/', 'location_history'),
    #url(r'api/update_database/','update_database'),
    
    
    url(r'api/reset/','reset_database'),
    url(r'api/trips/','trip_history'),

    url(r'$', 'index'),
    
)