var map;
var path;
var total_locations = [];
function initialize() {
    var mapOptions = {
        center: new google.maps.LatLng(39.8282, -98.5795),
        zoom: 4,
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
    $.getJSON('api/location_history/', function(data){
        $.each(data, function(i, obj) {
            obj['timestamp'] = obj['timestamp'];
            total_locations.push(obj);
        });
        var end = new Date(total_locations[0]['timestamp']);
        $( "#end_date" ).val( (end.getMonth() + 1) + '/' + end.getDate() + '/' + end.getFullYear());
        var start = new Date(total_locations[total_locations.length-1]['timestamp']);
        $( "#start_date" ).val( (start.getMonth() + 1) + '/' + start.getDate() + '/' + start.getFullYear()); 
        updateMap();
    
    });
    
    
    
    
}

function updateMap(resize){
    path.setMap(null);
    
    var start = Number(new Date($('#start_date').val()).getTime());
    var end = Number(new Date($('#end_date').val()).getTime());
    var layovers = $('#layovers').is(':checked');
    
    
    var f;
    for (f = 0; f < total_locations.length; f++) 
        if (end >= total_locations[f]['timestamp']) break;

    var s;
    for (s = total_locations.length - 1; s >= 0; s--) 
        if (start <= total_locations[s]['timestamp']) break; 
    
    var locations = []
    for (var i = f; i <= s; i++) {
        if (!layovers)
            if (total_locations[i]['layover']) 
                continue;
            
        locations.push(new google.maps.LatLng(total_locations[i]['lat'], total_locations[i]['long']));
    }
    
    
    path = null;         
    path = new google.maps.Polyline({
            path: locations,
            geodesic: true,
            strokeColor: '#FF0000',
            strokeOpacity: 1.0,
            strokeWeight: 2
        });
    path.setMap(map);
    if (resize)
        zoomToObject(path);
    
    locations = null;
    
    var window_start = new Date(total_locations[s]['timestamp']);
    var window_end = new Date(total_locations[f]['timestamp']);
    

    $( "#start_date" ).datepicker("destroy");
    $( "#end_date" ).datepicker("destroy");
    $( "#start_date" ).datepicker({minDate:window_start, maxDate:window_end});
    $( "#end_date" ).datepicker({minDate:window_start, maxDate:window_end});
    $( "#start_date" ).change(function () {updateMap(true)});
    $( "#end_date" ).change(function () {updateMap(true)});
    $( "#layovers" ).change(function () {updateMap(false)});
    
    var end = new Date(total_locations[0]['timestamp']);

    
    $('#info-panel').text('Last updated on ' + (end.getMonth() + 1) + '/' + end.getDate() + '/' + end.getFullYear());
    $('#info-panel').show();
    $('#control-panel').show();
    $( "#loading-area" ).isLoading( "hide" );
}


$(function() {
    
    $('#info-panel').hide();
    $('#control-panel').hide();
    google.maps.event.addDomListener(window, 'load', initialize);
    path = new google.maps.Polyline();


    pullMap();

    $( "#loading-area" ).isLoading({
        position: "overlay"
    });    

});


    
    
        
        
        
        
        