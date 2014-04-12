//var google_map_url = 'http://maps.googleapis.com/maps/api/staticmap?&zoom=6&size=600x300&markers=color:blue|%s,%s&sensor=true'
var google_map_url = 'http://maps.google.com/maps?&z=6&q=loc:%s,%s'

function init_carousels() {
  var sync2 = $("#control-carousel");
 
    options = {
        items : 7,
        lazyLoad: true,
        lazyEffect: false,
        itemsDesktop      : [1199,10],
        itemsDesktopSmall     : [979,10],
        itemsTablet       : [768,8],
        itemsMobile       : [479,4],
        pagination:false,
        //autoHeight:true,
        responsiveRefreshRate : 100,
    }
  if (! isMobile.any() ){
    options.navigation = true;
  }


  sync2.owlCarousel(options);
 
 
}

function get_flickr_photos() {
    $.getJSON( flickr_api_get_photos, function( data ) {

    photos = data['photoset']['photo'];
    $.each( photos, function( key, val ) {
        var medium_photo_url = 'http://farm' + val['farm'] + '.staticflickr.com/' + val['server']+ '/' + val['id'] + '_' + val['secret'] + '_m.jpg'; 
                
        var elem = '<div><a class="carousel-img"><img class="lazyOwl" data-src="%s" data-lat="%s" data-long="%s" data-datetaken="%s"></img></a></div>'
        $('#control-carousel').append(sprintf(elem, medium_photo_url, val['latitude'], val['longitude'], val['datetaken']));
    });

    $('.carousel-img').on('click', function () {
        var img = $(this).children('img')
        var small_image_url = img.attr('src');
        var large_image_url = small_image_url.slice(0,small_image_url.length-5) + 'b.jpg';
        $('#main-photo').empty();
        $('#main-photo').append('<img src="' + large_image_url + '">');
        
        var lat = img.attr('data-lat');
        var lon = img.attr('data-long');
        if ( lat != '0' || lon != '0'){
            var map_link = '<a title="Taken on %s "class="map-link" href="' + sprintf(google_map_url, lat, lon) + '">See where this was taken</a>'
            $('#main-photo').append(sprintf(map_link, img.attr('data-datetaken')));
            $('.map-link').magnificPopup({type:'iframe'});
        }
        
        

    });

    init_carousels();
    $(document).ready(function() {
        
    });

    
});

}


$(function() { 

    get_flickr_photos();

    
});

