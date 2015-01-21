import datetime

from django.db import models

# Create your models here.

class LocationHistoryPoint(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.BigIntegerField()
    
    def to_dict(self):
        return {'timestamp':self.timestamp, 'long':longitude, 'lat':self.latitude}

    def __unicode__(self):
        return datetime.datetime.fromtimestamp(self.timestamp/1000).isoformat()

class Flight(models.Model):
    origin_name = models.CharField(max_length = 30)
    origin_lat = models.FloatField()
    origin_long = models.FloatField()
    dest_name = models.CharField(max_length = 30)
    dest_lat = models.FloatField()
    dest_long = models.FloatField()
    date = models.DateField()
    work = models.BooleanField()
    title = models.CharField(max_length = 30)
            
            
    def build_from_json(self, json):
        self.origin_name = json['origin']
        self.origin_lat = float(json['origin_coords'][1:-1].split(',')[0])
        self.origin_long = float(json['origin_coords'][1:-1].split(',')[1])
        self.dest_name = json['destination']
        self.dest_lat = float(json['destination_coords'][1:-1].split(',')[0])
        self.dest_long = float(json['destination_coords'][1:-1].split(',')[1])
        self.date = datetime.datetime.strptime(json['date'], '%m-%d-%y').date()
        self.work = True if json['work'] == 'True' else False
        self.title = json['title']
    
    def build_return_flight(self, outgoing, date):
        self.origin_name = outgoing.dest_name
        self.origin_lat = outgoing.dest_lat
        self.origin_long = outgoing.dest_long
        self.dest_name = outgoing.origin_name
        self.dest_lat = outgoing.origin_lat
        self.dest_long = outgoing.origin_long
        self.date = datetime.datetime.strptime(date, '%m-%d-%y').date()
        self.work = outgoing.work
        self.title = "Returning - %s" % outgoing.title 
    
    def to_dict(self):
        return {'origin_name':self.origin_name, 'origin_lat':self.origin_lat, 'origin_long':self.origin_long, 'dest_name':self.dest_name, 'dest_lat':self.dest_lat, 'dest_long':self.dest_long, 'date':self.date.strftime('%m-%d-%y'), 'work':str(self.work), 'title':self.title}
        
    def __unicode__(self):
        return '%s: from %s to %s on %s' % (self.title, self.origin_name, self.dest_name, self.date)

class Distance(models.Model):
    point_a = models.CharField(max_length = 30)
    point_b = models.CharField(max_length = 30)
    distance_km = models.IntegerField(default = -1)
    
    def to_dict(self):
        return {'a':self.point_a, 'b':self.point_b, 'mi':int(self.distance_km * .621371)}
        
    def __unicode__(self):
        return '%s to %s' % (self.point_a, self.point_b)