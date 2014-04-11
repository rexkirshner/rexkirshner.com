var google_map_url = 'http://maps.googleapis.com/maps/api/staticmap?&zoom=6&size=600x300&markers=color:blue|%s,%s&sensor=true'


function get_flickr_photos() {


    $.getJSON( flickr_api_get_photos, function( data ) {
        
        photos = data['photoset']['photo'];
        $.each( photos, function( key, val ) {
            var tiny_photo_url = 'http://farm' + val['farm'] + '.staticflickr.com/' + val['server']+ '/' + val['id'] + '_' + val['secret'] + '_s.jpg';
            var medium_photo_url = 'http://farm' + val['farm'] + '.staticflickr.com/' + val['server']+ '/' + val['id'] + '_' + val['secret'] + '_m.jpg'; 
            var large_photo_url = 'http://farm' + val['farm'] + '.staticflickr.com/' + val['server']+ '/' + val['id'] + '_' + val['secret'] + '_b.jpg';
                if (val['latitude'] != '0' && val['longitude'] !='0'){
                    
                    var main_photo = '<li><p class="flex-caption"><a title="Taken on ' + val['datetaken'] + '"class="map-link" href="' + sprintf(google_map_url, val['latitude'], val['longitude']) + '">Check where this was taken</a></p><image class="lazy" data-src="' + large_photo_url + '"></image></li>'  
                } else {
                    var main_photo = '<li><image class="lazy" data-src="' + large_photo_url + '"></image></li>'  
                }
                $('#main-photo > ul:last').append(main_photo);
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
                $("img.lazy").slice(0,6).each(function () {
                    var src = $(this).attr("data-src");
                    $(this).attr("src", src).removeAttr("data-src").removeClass("lazy");
                });
            },
            before: function (slider) {
                // lazy load
                $("img.lazy").slice(0,5).each(function () {
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
            titleSrc: 'title'
          }
        });
    });  

}

$(function() {
    get_flickr_photos();
});

