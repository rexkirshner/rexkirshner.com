import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from models import Photo, PhotoForm
import settings

    
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


def index(request):
            
    return render_to_response("photos/photos.html",
                              {'flickr':settings.FLICKR_INFO},
                              context_instance=RequestContext(request))    
 