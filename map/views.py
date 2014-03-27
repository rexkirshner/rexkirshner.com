import json, urllib2
from math import radians, cos, sin, asin, sqrt

from django.shortcuts import render_to_response
from django.template import RequestContext

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    
    lon1, lat1, lon2, lat2 = map(lambda x: x / 10000000 , [lon1, lat1, lon2, lat2])
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
        data = json.loads(data)
        self.locations = data['locations']
    
    def simplify(self):
        simple_locations = []
        for loc in self.locations:
            simple_locations.append({'timestampMs':loc['timestampMs'], 'longitudeE7':loc['longitudeE7'], 'latitudeE7':loc['latitudeE7']})
        self.locations = simple_locations
        
    def closest_points(self, km = 25):
        new_locations = [self.locations[0]]
        for loc in self.locations[1:]:
            distance = haversine(new_locations[-1]['longitudeE7'],new_locations[-1]['latitudeE7'],loc['longitudeE7'],loc['latitudeE7']) 
            if distance > km:
                new_locations.append(loc)
        self.locations = new_locations
    
    def js(self):
        ret = 'location_history = ['
        for loc in self.locations:
            ret += '{"timestamp":%s, lat: %s, long %s},' % (loc['timestampMs'], loc['latitudeE7'] / 10000000.0, loc['longitudeE7'] / 10000000.0)
        ret += ']'
        return ret

def location_history(request):
    
    url = 'https://dl.dropboxusercontent.com/u/28618487/mapper/LocationHistory.json'
    data = urllib2.urlopen(url).read()
    p = Parser(data)
    p.closest_points()
    #js = p.js()
    
    return render_to_response("map/location_history.html",
                              {'location_history':p.locations,},
                              context_instance=RequestContext(request))