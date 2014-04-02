from django.conf.urls import patterns, include, url


urlpatterns = patterns('photos.views',
    url(r'$', 'index'),
    
)