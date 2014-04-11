import settings, hashlib


    
    
    
    
    
  
    

if __name__ == '__main__':
    flickr_request = { 'auth_token':'72157643776644984-a53d8e520bd7833a','method': 'flickr.people.getPublicPhotos', 'user_id':settings.FLICKR_INFO['user_id'], 'extras':'date_taken,geo', 'format':'json', 'nojsoncallback':'1'}
    print flickr_generate_url(flickr_request)