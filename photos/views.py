import datetime, hashlib, urllib2, json

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from models import FlickrAuthToken, Photo, PhotoForm

import settings

def flickr_generate_url(params, defaults = True):
    if defaults:
        params['format'] = 'json'
        params['nojsoncallback'] = '1'    
        if FlickrAuthToken.objects.all().count() > 0:
            params['auth_token'] = FlickrAuthToken.objects.all()[0].token

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
    
    
    
    return render_to_response("photos/report_auth.html",
                              {'flickr':settings.FLICKR_INFO, 'url':auth_url, 'auth_token': auth_token},
                              context_instance=RequestContext(request))  

def flickr_api(request):
    if request.method == 'GET':
        params = {}
        num_params = int(request.GET.get('num-params'))
        for i in range(num_params):
            params[request.GET.get('param-%d' % i)] = request.GET.get('value-%d' % i)
        
        url = flickr_generate_url(params, False)
        flickr_response = urllib2.urlopen(url).read()
        flickr_json_response = json.loads(flickr_response)
        
        response = HttpResponse(content = json.dumps({'url':url, 'response':flickr_json_response}), content_type='application/json')
        return response
        

def flickr_api_test(request):
    if FlickrAuthToken.objects.all().count() > 0:
        token = FlickrAuthToken.objects.all()[0]
    else:
        token = None
    return render_to_response("photos/flickr_api.html",
                              {'token':token},
                              context_instance=RequestContext(request)) 
                                



def index(request):
    params = {'method':'flickr.photosets.getPhotos','photoset_id':'72157643363289374', 'extras':'date_taken,geo'}
    flickr_api_get_photos = flickr_generate_url(params)
    
    return render_to_response("photos/photos.html",
                              {'flickr_api_get_photos':flickr_api_get_photos},
                              context_instance=RequestContext(request))    
 