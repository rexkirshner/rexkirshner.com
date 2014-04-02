import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from models import Photo, PhotoForm

    
def index(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('photos.views.index'))
    else:
         form = PhotoForm()
    f = PhotoForm
    return render_to_response("photos/photos.html",
                              {'form':form},
                              context_instance=RequestContext(request))

def upload_photo(request):
    pass