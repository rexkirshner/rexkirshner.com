from django.conf.urls import patterns, include, url


urlpatterns = patterns('photos.views',
    url(r'upload/', 'upload_photo'),
    url(r'flickr/auth/frob/','gather_frob'),
    url(r'flickr/auth/', 'generate_oauth_token'),
    url(r'flickr/api/', 'flickr_api'),
    url(r'flickr/', 'flickr_api_test'),
    
    
    url(r'$', 'index'),
    
    
)