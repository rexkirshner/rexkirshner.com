from django.db import models

from google.appengine.ext import blobstore


# Create your models here.


class Photo(models):
    datetime =  models.DateTimeField()
    