from django.shortcuts import render, render_to_response
from givers.models import Giver
from math import sin, cos, radians, degrees, acos, sqrt
import json

#import urllib2

# Create your views here.
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    if request.method == 'POST':
        return render(request, 'search.html')

def search(request, lat_start="43.722598", lng_start="-79.645825", lat_end="43.851361", lng_end="-79.332975"):
    all_givers = Giver.objects.all()
    nearby_givers = []
    giver_ratings = []
    MAX_RADIUS = 0.11

    for giver in all_givers:
        hyp_from_start = calc_hypotenuse(float(lat_start), float(lng_start), float(giver.lat_start), float(giver.lng_start))
        hyp_from_dest = calc_hypotenuse(float(lat_end), float(lng_end), float(giver.lat_end), float(giver.lng_end))
        if hyp_from_start <= MAX_RADIUS and hyp_from_dest <= MAX_RADIUS:
            rating = 50*(hyp_from_start/MAX_RADIUS) + 50*(hyp_from_dest/MAX_RADIUS)
            giver_ratings.append(rating)
            nearby_givers.append(giver.fb_id)

    givers_zip_ratings = zip(nearby_givers, giver_ratings)
    #dump = json.dumps(givers_zip_ratings)
    dump = json.dumps('[["545547692", 86.4365540305593], ["592257540", 71.67730794690695], ["733050239", 75.02406966663716], ["100002131130870", 83.35098178107881], ["1645560180", 91.70583373342106], ["715076506", 75.73249881179504], ["517765107", 37.01613186970565], ["10204097819428052", 37.089990452084265]]')

    return render(request, 'index.html', dump)

def post_user(request):
    fbID = request.POST.get('fb_id', False).encode('utf8')
    obj = Giver.objects.filter(fb_id=fbID)
    if not obj:
        obj = Giver(fb_id=fbID, lng_start="-79.645825", lat_start="43.722598", lng_end="-79.258499", lat_end="43.884701")
        obj.save()
    return render(request, 'index.html')

def calc_hypotenuse(lat_a, long_a, lat_b, long_b):
    hyp = sqrt((lat_a-lat_b)*(lat_a-lat_b) + (long_a-long_b)*(long_a-long_b))
    return hyp

def calc_dist(lat_a, long_a, lat_b, long_b):
    lat_a = radians(lat_a)
    lat_b = radians(lat_b)
    long_diff = radians(long_a - long_b)
    distance = (sin(lat_a) * sin(lat_b) +
                cos(lat_a) * cos(lat_b) * cos(long_diff))
    return degrees(acos(distance)) * 69.09


#def facebook_login(request):
#    url = 'https://www.facebook.com/dialog/oauth?client_id=1486567314893292&redirect_uri=https://www.facebook.com/connect/login_success.html&response_type=token&scope=public_profile,email,user_friends'
#    serialized_data = urllib2.urlopen(url).read()

#    data = json.loads(serialized_data)
#    r = request.GET("https://www.facebook.com/dialog/oauth?client_id=1486567314893292&redirect_uri=https://www.facebook.com/connect/login_success.html&response_type=token&scope=public_profile,email,user_friends")
#    return render(request, 'search.html')