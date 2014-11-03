import urllib2, datetime, random
from math import radians, cos, sin, asin, sqrt

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse



import settings

import base_trips

from models import Flight

def reset_database(request):
    Flight.objects.all().delete()
    num = 0
    for trip_wrapper in base_trips.flights['flights']:
        trip = trip_wrapper['flight']
        new_flight = Flight()
        new_flight.build_from_json(trip)
        new_flight.save()
        num += 1
        if trip['round-trip'] == 'True':
            new_return_flight = Flight()
            new_return_flight.build_return_flight(new_flight, trip['return'])
            new_return_flight.save()
            num += 1
    recap = 'num of entries added: %d' % num
    
    return HttpResponse(recap)

def trip_history(request):
    legs = Flight.objects.all().order_by('-date')
    legs_json = []
    location_counts = {}
    i = 0
    for leg in legs:
        if i % 1 == 0:
            o_num_times = location_counts.get(leg.origin_name,0)
            leg.origin_lat += random.uniform(-.006 * o_num_times, .006 * o_num_times)
            leg.origin_long += random.uniform(-.0025 * o_num_times, .0025 * o_num_times)
            location_counts[leg.origin_name] = o_num_times + 1
        else:
            d_num_times = location_counts.get(leg.dest_name,0)
            leg.dest_lat += random.uniform(-.006 * d_num_times, .006 * d_num_times)
            leg.dest_long += random.uniform(-.0025 * d_num_times, .0025 * d_num_times)

            location_counts[leg.dest_name] = d_num_times + 1
        
        legs_json.append({'trip':leg.to_dict()})
        #location_counts['St. Louis'] = 0
        i += 1
    response = HttpResponse(str(legs_json).replace("'", '"').replace('u"', '"'))
    return response

def index(request):
    return render_to_response("map/map2.html",
                              {},
                              context_instance=RequestContext(request))



























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
            time = int(self.locations[i]['timestampMs'])
            long = self.locations[i]['longitudeE7'] / 10000000.0
            lat = self.locations[i]['latitudeE7'] / 10000000.0
            self.locations[i] = {'timestamp':time, 'long':long, 'lat':lat}

    def find_new_entries(self, latest_saved = None, earliest_saved = None):
        if latest_saved:
            for i in range(len(self.locations)):
                new_data_point_1 = 0
                if self.locations[i]['timestamp'] <= latest_saved.timestamp:
                    new_data_point_1 = i
                    break
                
        else:
            new_data_point = len(self.locations)
        
        if earliest_saved:
            x = range(len(self.locations))
            x.reverse()
            for i in x:
                new_data_point_2 = len(self.locations)
                if self.locations[i]['timestamp'] >= earliest_saved.timestamp:
                    new_data_point_2 = i
                    break  
        else:
            new_data_point_2 = 0
        
        return self.locations[:new_data_point_1] + self.locations[new_data_point_2:]
              
class Analyzer(object):
    
    def __init__(self, data):
        if type(data) is list:
            self.locations = data
        else:
            self.locations = []
            for loc in data:
                self.locations.append(loc.to_dict())
        if settings.COMPRESS:
            self._closest_points(settings.COMPRESS_MIN_KM)
        
    def _closest_points(self, km = 25):
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
            
            
            if self.locations[i]['timestamp'] < bb and self.locations[i]['timestamp'] > aa:
                
                self.locations[i]['layover'] = True
        
        for i in range(1, len(i_of_flight_arrival)):
            time_delta = self.locations[i_of_flight_arrival[i-1]]['timestamp'] - self.locations[i_of_flight_arrival[i]]['timestamp']
            if time_delta < min_time:
                for j in range( i_of_flight_arrival[i-1], i_of_flight_arrival[i]+1):
                    self.locations[j]['layover'] = True
                    pass
        
        
            
    def json(self):
        return  simplejson.dumps(self.locations) 
    
def location_history(request):
    if settings.USE_DB:
        data = LocationHistoryPoint.objects.all().order_by('-timestamp')
    else:
        url = 'https://dl.dropboxusercontent.com/u/28618487/mapper/LocationHistory.json'

        data = urllib2.urlopen(url).read()
        p = Parser(data)
        data = p.locations
    
    a = Analyzer(data)
    a.identify_layovers()
    response = HttpResponse(a.json())
    
    return response

def update_database(request):
    url = 'https://dl.dropboxusercontent.com/u/28618487/mapper/LocationHistory.json'

    data = urllib2.urlopen(url).read()
    p = Parser(data)
    try:
        latest_point = LocationHistoryPoint.objects.all().order_by('-timestamp')[0]
        try:
            earliest_point = LocationHistoryPoint.objects.all().order_by('-timestamp')[LocationHistoryPoint.objects.all().count() - 1]
        except IndexError:
            earliest_point = None

    except IndexError:
        latest_point = None

    new_entries = p.find_new_entries(latest_point, earliest_point)
    for entry in new_entries:
        add = LocationHistoryPoint(latitude = entry['lat'], longitude = entry['long'], timestamp = entry['timestamp'])
        add.save()
    
    recap = 'num of new entires: %d <br />total number of entries: %d <br />total number of entries in doc: %d <br />' % (len(new_entries), LocationHistoryPoint.objects.count(), len(p.locations))
    if earliest_point:
        recap += 'earliest_point: %s (%s)<br />' % (datetime.datetime.fromtimestamp(earliest_point.timestamp/1000).isoformat(), earliest_point.timestamp)
    if latest_point:
        recap += 'latest_point: %s (%s)<br />' % (datetime.datetime.fromtimestamp(latest_point.timestamp/1000).isoformat(), latest_point.timestamp)
    
    return HttpResponse(recap)
    





  
    
    
    
    
    
    
    
    
    
    
    
    
    