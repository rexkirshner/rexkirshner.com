import urllib2, datetime
from math import radians, cos, sin, asin, sqrt

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse

from models import LocationHistoryPoint

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 

    # 6367 km is the radius of the Earth
    km = 6367 * c
    return km

class Parser(object):
    
    def __init__(self, data):
        data = simplejson.loads(data)
        self.locations = data['locations']
        self._simplify()
    
    def _simplify(self):
        for i in range(len(self.locations)):
            time = self.locations[i]['timestampMs']
            long = self.locations[i]['longitudeE7'] / 10000000.0
            lat = self.locations[i]['latitudeE7'] / 10000000.0
            self.locations[i] = {'timestamp':time, 'long':long, 'lat':lat}

    def find_new_entries(self, latest_saved = None):
        if latest_saved:
            for i in range(len(self.locations)):
                new_data_point = 0
                if int(self.locations[i]['timestamp']) <= int(latest_saved.timestamp):
                    new_data_point = i
                    break
                
        else:
            new_data_point = len(self.locations)
        
        return self.locations[:new_data_point]
              
class Analyzer(object):
    
    def __init__(self, data):
        self.locations = []
        for loc in data:
            self.locations.append({'timestamp':loc.timestamp, 'long':loc.longitude, 'lat':loc.latitude})
        
    def closest_points(self, km = 25):
        new_locations = [self.locations[0]]
        for loc in self.locations[1:]:
            distance = haversine(new_locations[-1]['long'],new_locations[-1]['lat'],loc['long'],loc['lat']) 
            if distance > km:
                new_locations.append(loc)
        self.locations = new_locations
    
    def identify_layovers(self, min_hours = 12, flight_distance = 350):
        min_time = min_hours * 60 * 60 * 1000
        
        i_of_flight_arrival = []        
        for i in range(1,len(self.locations)):
            self.locations[i]['layover'] = False
            distance = haversine(self.locations[i-1]['long'],self.locations[i-1]['lat'],self.locations[i]['long'],self.locations[i]['lat'])
            if distance > flight_distance:
                i_of_flight_arrival.append(i)
            
            ############## Manual Fixes ##############
            
            ##          NJ after boat trip          ##
            a = datetime.datetime(year=2013, month=7, day=12, hour=0)
            aa = int(a.strftime("%s")) * 1000
            b = datetime.datetime(year=2013, month=7, day=13, hour=12)
            bb = int(b.strftime("%s")) * 1000
            
            
            if int(self.locations[i]['timestamp']) < bb and int(self.locations[i]['timestamp']) > aa:
                
                self.locations[i]['layover'] = True
        
        for i in range(1, len(i_of_flight_arrival)):
            time_delta = int(self.locations[i_of_flight_arrival[i-1]]['timestamp']) - int(self.locations[i_of_flight_arrival[i]]['timestamp'])
            if time_delta < min_time:
                for j in range( i_of_flight_arrival[i-1], i_of_flight_arrival[i]+1):
                    self.locations[j]['layover'] = True
                    pass
        
        
            
    def json(self):
        return  simplejson.dumps(self.locations) 
    
def index(request):
    return render_to_response("map/map.html",
                              {},
                              context_instance=RequestContext(request))

def location_history(request):
    data = LocationHistoryPoint.objects.all().order_by('-timestamp')
    a = Analyzer(data)
    a.identify_layovers()
    response = HttpResponse(a.json())
    return response

def update_database(request):
    url = 'https://dl.dropboxusercontent.com/u/28618487/mapper/LocationHistory.json'

    data = urllib2.urlopen(url).read()
    p = Parser(data)
    try:
        latest_point = LocationHistoryPoint.objects.latest('timestamp')
    except LocationHistoryPoint.DoesNotExist:
        latest_point = None
    new_entries = p.find_new_entries(latest_point)
    for entry in new_entries:
        add = LocationHistoryPoint(latitude = entry['lat'], longitude = entry['long'], timestamp = entry['timestamp'])
        add.save()
    return HttpResponse('num of new entires: %d <br />total number of entries: %d <br />total number of entries in doc: %d <br />' % (len(new_entries), LocationHistoryPoint.objects.count(), len(p.locations)))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    