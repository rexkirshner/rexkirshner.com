import datetime 

from django.db import models
from django.forms import ModelForm

from blobstore_storage.storage import BlobStoreStorage

from settings import UPLOAD_TO

# Create your models here.

class FlickrAuthToken(models.Model):
    date_created = models.DateTimeField(default = datetime.datetime.now())
    token = models.CharField(max_length = 100)
    nsid = models.CharField(max_length = 25)
    


class Photo(models.Model):
    upload_time = models.DateTimeField(default = datetime.datetime.now())
    photo = models.ImageField(storage=BlobStoreStorage(), upload_to=UPLOAD_TO, max_length=255)
    def __unicode__(self):
        index = self.photo.name.find('/' + UPLOAD_TO)
        if index > -1:
            return self.photo.name[len(UPLOAD_TO) + index + 2:]

        return self.photo.name
    
        
class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        exclude = ['upload_time']
    
        
        
    

    