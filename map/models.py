import datetime

from django.db import models

# Create your models here.

class LocationHistoryPoint(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.CharField(max_length=14)
    
    def to_dict(self):
        return {'timestamp':self.timestamp, 'long':longitude, 'lat':self.latitude}

    def __unicode__(self):
        return datetime.datetime.fromtimestamp(int(self.timestamp)/1000).isoformat()
      