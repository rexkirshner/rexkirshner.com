function get_flickr_photos() {
    var url = "https://api.flickr.com/services/rest/?method=flickr.people.getPublicPhotos&api_key=" + flickr_api_key + "&user_id=" + flickr_user_id + "&format=json&nojsoncallback=1";
    
    
    $.getJSON( url, function( data ) {
      photos = data['photos']['photo'];
      $.each( photos, function( key, val ) {
        var tiny_photo_url = 'http://farm' + val['farm'] + '.staticflickr.com/' + val['server']+ '/' + val['id'] + '_' + val['secret'] + '_s.jpg';
        var photo_url = 'http://farm' + val['farm'] + '.staticflickr.com/' + val['server']+ '/' + val['id'] + '_' + val['secret'] + '_z.jpg';
        photo_urls.push(photo_url);
        $('#photos > tbody:last').append('<tr><td><image src="' + tiny_photo_url + '"></image></td><td><a href="' + photo_url + '">Link</a></td></tr>');
      });

    });  
    
    $('#test').text(url);

}


var photo_urls = [];

$(function() {
    get_flickr_photos();

});

