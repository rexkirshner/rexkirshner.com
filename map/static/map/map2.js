var map;
var paths = [];
var total_locations = [];
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
        $.each(data, function(i, obj) {
            
            total_locations.push(obj['trip']);
        });
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


$(function() {
    
    google.maps.event.addDomListener(window, 'load', initialize);

    $( "#loading-area" ).isLoading({position: "overlay"});    

    pullMap();


});


    
    
        
        
        
        
        