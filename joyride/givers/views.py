from django.shortcuts import render
from givers.models import Giver

#import urllib2
#import json

# Create your views here.
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    if request.method == 'POST':
        return render(request, 'search.html')

def search(request):
    return render(request, 'search.html')

def post_user(request):
    fbID = request.POST.get('fb_id', False).encode('utf8')+"0006"
    g = Giver(fb_id=fbID, lng_start="-79.645825", lat_start="43.722598", lng_end="-79.258499", lat_end="43.884701")
    g.save()
    return render(request, 'index.html')



#def facebook_login(request):
#    url = 'https://www.facebook.com/dialog/oauth?client_id=1486567314893292&redirect_uri=https://www.facebook.com/connect/login_success.html&response_type=token&scope=public_profile,email,user_friends'
#    serialized_data = urllib2.urlopen(url).read()

#    data = json.loads(serialized_data)
#    r = request.GET("https://www.facebook.com/dialog/oauth?client_id=1486567314893292&redirect_uri=https://www.facebook.com/connect/login_success.html&response_type=token&scope=public_profile,email,user_friends")
#    return render(request, 'search.html')