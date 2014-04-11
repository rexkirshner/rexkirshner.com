import datetime, hashlib, urllib2, json

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from models import FlickrAuthToken, Photo, PhotoForm

import settings

def flickr_generate_url(params):    
    api_sig = settings.FLICKR_INFO['secret'] + 'api_key' + settings.FLICKR_INFO['api_key']
    url = 'https://api.flickr.com/services/rest/?api_key=%s&' % settings.FLICKR_INFO['api_key']
    
    for key in sorted(params.keys()):
        api_sig += key + params[key]
        url += key + '=' + params[key] + '&'
    
    m = hashlib.md5()
    m.update(api_sig)
    api_sig = m.hexdigest()
    
    url += 'api_sig=' + api_sig
    
    return url

def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('photos.views.index'))
    else:
         form = PhotoForm()
    f = PhotoForm
    return render_to_response("photos/upload_photo.html",
                              {'form':form},
                              context_instance=RequestContext(request))    

def generate_oauth_token(request):
    flickr = settings.FLICKR_INFO
    permission = 'read'
    flickr['perms'] = permission
    m = hashlib.md5()
    m.update(flickr['secret'] + 'api_key' + flickr['api_key'] + 'perms' + flickr['perms'])
    flickr['api_sig'] = m.hexdigest()
    
    
    return render_to_response("photos/authenticate.html",
                              {'flickr':settings.FLICKR_INFO},
                              context_instance=RequestContext(request))    

def gather_frob(request):
    frob = request.GET.get('frob','Frob not found')
    
    params = {'format':'json', 'nojsoncallback':'1', 'frob':frob, 'method':'flickr.auth.getToken'}    
    auth_url = flickr_generate_url(params)
    
    response = urllib2.urlopen(auth_url)
    auth_token = json.loads(response.read())
    
    
    try:
        past_token = FlickrAuthToken.objects.get(nsid=auth_token['auth']['user']['nsid'])
        past_token.delete()
    except FlickrAuthToken.DoesNotExist:
        pass
    
    new_token = FlickrAuthToken()
    new_token.token = auth_token['auth']['token']['_content']
    new_token.nsid = auth_token['auth']['user']['nsid']
    new_token.save()
    
    
    
    return render_to_response("photos/gather_frob.html",
                              {'flickr':settings.FLICKR_INFO, 'url':auth_url, 'auth_token': auth_token},
                              context_instance=RequestContext(request))  


def index(request):
            
    return render_to_response("photos/photos.html",
                              {'flickr':settings.FLICKR_INFO},
                              context_instance=RequestContext(request))    
 