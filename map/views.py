import urllib2, datetime
from math import radians, cos, sin, asin, sqrt

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse

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
        
    def closest_points(self, km = 25):
        new_locations = [self.locations[0]]
        for loc in self.locations[1:]:
            distance = haversine(new_locations[-1]['longitudeE7'],new_locations[-1]['latitudeE7'],loc['longitudeE7'],loc['latitudeE7']) 
            if distance > km:
                new_locations.append(loc)
        self.locations = new_locations
    
    
    

def index(request):
    
    return render_to_response("map/map.html",
                              {},
                              context_instance=RequestContext(request))

def location_history(request):
    url = 'https://dl.dropboxusercontent.com/u/28618487/mapper/LocationHistory.json'

    data = urllib2.urlopen(url).read()
    p = Parser(data)
    
    kml_start = '''
        <?xml version="1.0" encoding="UTF-8"?>
        <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
        <Document>
        <name>Location history from 02/15/1976 to 03/26/2014</name>
        <open>1</open>
        <description/>
        <StyleMap id="multiTrack">
        <Pair>
        <key>normal</key>
        <styleUrl>#multiTrack_n</styleUrl>
        </Pair>
        <Pair>
        <key>highlight</key>
        <styleUrl>#multiTrack_h</styleUrl>
        </Pair>
        </StyleMap>
        <Style id="multiTrack_n">
        <IconStyle>
        <Icon>
        <href>http://earth.google.com/images/kml-icons/track-directional/track-0.png</href>
        </Icon>
        </IconStyle>
        <LineStyle>
        <color>99ffac59</color>
        <width>6</width>
        </LineStyle>
        </Style>
        <Style id="multiTrack_h">
        <IconStyle>
        <scale>1.2</scale>
        <Icon>
        <href>http://earth.google.com/images/kml-icons/track-directional/track-0.png</href>
        </Icon>
        </IconStyle>
        <LineStyle>
        <color>99ffac59</color>
        <width>8</width>
        </LineStyle>
        </Style>
        <Placemark>
        <name>Latitude User</name>
        <description>Location history for Latitude User from 02/15/1976 to 03/26/2014</description>
        <styleUrl>#multiTrack</styleUrl>
        <gx:Track>
        <altitudeMode>clampToGround</altitudeMode>
    '''
    
    kml_end = '''
    </gx:Track>
    </Placemark>
    </Document>
    </kml>
    '''
    
    kml_body = ''
    for loc in p.locations:
        kml_body += '<gx:coord>%s %s 0</gx:coord>' % (loc['long'], loc['lat'])
    
    
    response = HttpResponse(kml_start + kml_body + kml_end, content_type='application/vnd.google-earth.kml+xml')
    response['Content-Disposition'] = 'attachment; filename="location_history.kml"'
    
    return response
    
    #p.closest_points()
    
    #return render_to_response("map/location_history.kml",
    #                          {'location_history':p.locations,},
    #                          context_instance=RequestContext(request))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    