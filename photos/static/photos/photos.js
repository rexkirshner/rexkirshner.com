function get_flickr_photos() {
var url = "https://api.flickr.com/services/rest/?method=flickr.people.getPublicPhotos&api_key=" + flickr_api_key + "&user_id=" + flickr_user_id + "&extras=date_taken,geo&format=json&nojsoncallback=1";


$.getJSON( url, function( data ) {
    photos = data['photos']['photo'];
    $.each( photos, function( key, val ) {
        var tiny_photo_url = 'http://farm' + val['farm'] + '.staticflickr.com/' + val['server']+ '/' + val['id'] + '_' + val['secret'] + '_s.jpg';
        var medium_photo_url = 'http://farm' + val['farm'] + '.staticflickr.com/' + val['server']+ '/' + val['id'] + '_' + val['secret'] + '_m.jpg'; 
        var large_photo_url = 'http://farm' + val['farm'] + '.staticflickr.com/' + val['server']+ '/' + val['id'] + '_' + val['secret'] + '_b.jpg';
        //photo_urls.push(photo_url);
        //$('#photos > tbody:last').append('<tr><td><image src="' + tiny_photo_url + '"></image></td><td><a href="' + large_photo_url + '">Link</a></td></tr>');
        var google_map_url = 'http://maps.googleapis.com/maps/api/staticmap?&zoom=6&size=600x300&markers=color:blue|' + val['latitude'] + ',' + val['longitude'] + '&sensor=true'
        $('#main-photo > ul:last').append('<li><p class="flex-caption"><a title="Taken on ' + val['datetaken'] + '"class="map-link" href="' + google_map_url + '">Check where this was taken</a></p><image src="' + large_photo_url + '"></image></li>');
        $('#carousel > ul:last').append('<li><image class="lazy" data-src="' + medium_photo_url + '"></image></li>');

    });
    



    $('#carousel').flexslider({
        animation: "slide",
        controlNav: false,
        animationLoop: false,
        slideshow: false,
        itemWidth: 210,
        itemMargin: 5,
        asNavFor: "#main-photo",
        init: function (slider) {
            // lazy load
            $("img.lazy").slice(0,5).each(function () {
                var src = $(this).attr("data-src");
                $(this).attr("src", src).removeAttr("data-src").removeClass("lazy");
            });
        },
        before: function (slider) {
            // lazy load
            $("img.lazy").slice(0,3).each(function () {
                var src = $(this).attr("data-src");
                $(this).attr("src", src).removeAttr("data-src").removeClass("lazy");
            });
        }
    });

    $('#main-photo').flexslider({
        animation: "slide",
        controlNav: false,
        animationLoop: false,
        slideshow: false,
        sync: "#carousel",
        init: function (slider) {
            // lazy load
            $("img.lazy").slice(0,5).each(function () {
                var src = $(this).attr("data-src");
                $(this).attr("src", src).removeAttr("data-src").removeClass("lazy");
            });
        },
        before: function (slider) {
            // lazy load
            $("img.lazy").slice(0,3).each(function () {
                var src = $(this).attr("data-src");
                $(this).attr("src", src).removeAttr("data-src").removeClass("lazy");
            });
        }
    });  
    $('.map-link').magnificPopup({ 
      type: 'image',
      image: {
        // options for image content type
        titleSrc: 'title'
      }
    });
});  

$('#test').text(url);

}


var photo_urls = [];

$(function() {
    get_flickr_photos();
    $('#photos').hide();
    $('#table-toggle').click(function(){
        $('#photos').toggle();
    });
});

