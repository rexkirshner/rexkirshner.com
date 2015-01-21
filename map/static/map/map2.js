var map;
var paths = [];
var total_locations = [];
var distances = {};
var start_date;
var end_date;

function initialize() {
    var zoom_level = 5;
    if (isMobile.any() ){
        zoom_level = 3;
    }

    var mapOptions = {
        center: new google.maps.LatLng(39.8282, -98.5795),
        zoom: zoom_level,
        scrollwheel: false,
        disableDefaultUI: true,
        zoomControl: true,
        zoomControlOptions: {
            position: google.maps.ControlPosition.LEFT_CENTER
        },
    };
    map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

}

function zoomToObject(obj){
    var bounds = new google.maps.LatLngBounds();
    var points = obj.getPath().getArray();
    for (var n = 0; n < points.length ; n++){
        bounds.extend(points[n]);
    }
    map.fitBounds(bounds);
    setTimeout(function() {
                google.maps.event.trigger(map,'resize');
                map.fitBounds(bounds);
                }, 200);
}

function pullMap() {

    total_locations = [];
    $.getJSON('api/trips/', function(data){

        var x = 0;
        $.each(data['distances'], function(i, obj) {    
            var key = obj['distance']['a'] + '-' + obj['distance']['b'];
            var mi = parseInt(obj['distance']['mi']);
            distances[key] =  mi;
            x += 1;
        });
        var y = 0  ; 
        $.each(data['trips'], function(i, obj) {    
            total_locations.push(obj['trip']);
            y += 1;
        });
        
        start_date = new Date(data['start_date']);
        
        calcMapStats();

        updateMap();
    });
}

function updateMap(resize){
    for (var i = 0; i < total_locations.length; i++) {

        var trip_stops = [
            new google.maps.LatLng(total_locations[i]['origin_lat'], total_locations[i]['origin_long']),
            new google.maps.LatLng(total_locations[i]['dest_lat'], total_locations[i]['dest_long']),
        ];
        
        
        
        
        if (total_locations[i]['work'] == 'True') {
            var row = '<tr class="info">';
            var m = 'Yes'
            var color = "#00FF00"
        } else {
            var row = '<tr class="success">';
            var m = 'No'
            var color = "#0000FF"
        }
        
        var flight = new google.maps.Polyline({
            path:trip_stops,
            geodesic: true,
            //strokeColor: color,
            strokeColor: '#FF0000',
            strokeOpacity: .33,
            strokeWeight: 10
        });
        
        row += '<td>' + total_locations[i]['date'] + '</td>'
        row += '<td>' + total_locations[i]['title'] + '</td>'
        row += '<td>' + m + '</td>'
        row += '<td>' + total_locations[i]['origin_name'] + '</td>'
        row += '<td>' + total_locations[i]['dest_name'] + '</td>'
        row += '</tr>'
        
        $('#trip-table').append(row);
        
        flight.setMap(map);
        
        paths.push(flight);
    }
    //alert(paths.length);
    
    $( "#loading-area" ).isLoading( "hide" );
    
}

var oneDay = 24*60*60*1000; // hours*minutes*seconds*milliseconds

function diffDays (firstDate, secondDate) {
    
    return Math.round(Math.abs((firstDate.getTime() - secondDate.getTime())/(oneDay)));
}

function calcMapStats(){
    years = {}

    for (var i = 0; i <= new Date().getFullYear() - 2013; i++){
        years[2013 + i] = {'total_distance_traveled':0,
                           'num_flights':0,
                           'days_in':{},
                          };
    }    
    
    console.log(start_date);
    
    years[start_date.getFullYear()]['days_in']['St. Louis'] = diffDays(start_date, new Date(total_locations[total_locations.length - 1]['date']))
    
    for (var i = total_locations.length - 1; i >= 0; i--){
        var y = new Date(total_locations[i]['date']).getFullYear();
        var places = [total_locations[i]['origin_name'], total_locations[i]['dest_name']];
        places.sort();
        years[y]['total_distance_traveled'] += distances[places[0] + '-' + places[1]];
        
        years[y]['num_flights'] += 1;
        
        if (i > 0) {            
            if (!(total_locations[i]['dest_name'] in years[y]['days_in'])){
                years[y]['days_in'][total_locations[i]['dest_name']] = 0;
            } 
            
            var d1 = new Date(total_locations[i]['date']);
            var d2 = new Date(total_locations[i-1]['date']);
            
            if (d1.getFullYear() != d2.getFullYear()) {
                d2 = new Date(y, 11, 31, 23);
            }
            years[y]['days_in'][total_locations[i]['dest_name']] += diffDays(d1, d2)
        }
    }
    

    
    end_date = new Date(total_locations[0]['date'])

    if (end_date < new Date()){
        end_date = new Date();
    }
    
    years[end_date.getFullYear()]['days_in']['St. Louis'] += diffDays(new Date(total_locations[0]['date']), end_date);
        
}

function dispMapStats() {


}


$(function() {
    
    google.maps.event.addDomListener(window, 'load', initialize);

    $( "#loading-area" ).isLoading({position: "overlay"});    

    pullMap();

});



    
    
        
        
        
        
        