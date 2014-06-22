from django.shortcuts import render, render_to_response
from givers.models import Giver
from math import sin, cos, radians, degrees, acos, sqrt
import json
import urllib2

# Create your views here.
def index(request):
    # dump = json.dumps('[["545547692", 86.4365540305593], ["592257540", 71.67730794690695], ["733050239", 75.02406966663716], ["100002131130870", 83.35098178107881], ["1645560180", 91.70583373342106], ["715076506", 75.73249881179504], ["517765107", 37.01613186970565], ["10204097819428052", 37.089990452084265]]')
    dump = '[[{"fb_id": "545547692","rating": 86.4365540305593}],[{"fb_id": "592257540","rating": 71.67730794690695}],[{"fb_id": "733050239","rating": 75.02406966663716}],[{"fb_id": "100002131130870","rating": 83.35098178107881}],[{"fb_id": "1645560180","rating": 91.70583373342106}],[{"fb_id": "715076506","rating": 75.73249881179504}],[{"fb_id": "517765107","rating": 37.01613186970565}],[{"fb_id": "10204097819428052","rating": 37.089990452084265}]]'
    if request.method == 'GET':
        return render(request, 'index.html', {"dump" : dump})
    if request.method == 'POST':
        return render(request, 'search.html')

    return render(request, 'index.html')
    # return {
    #     "message": "Here is some text"
    # }


def search(request, lat_start="43.722598", lng_start="-79.645825", lat_end="43.851361", lng_end="-79.332975"):
    all_givers = Giver.objects.all()
    nearby_givers = []
    giver_fb_id = []
    giver_ratings = []
    giver_names = []
    giver_lat_start = []
    giver_lat_end = []
    giver_lng_start = []
    giver_lng_end = []

    MAX_RADIUS = 0.11
    GRAPH_API_BASE_URL = 'https://graph.facebook.com/'

    # Get starting latitude and longitude location
    if request.POST.get('StartingLocation'):
        GEOCODE_START_REQUEST_URL = 'http://maps.google.com/maps/api/geocode/json?address='+request.POST.get('StartingLocation', False).encode('utf8')+'&sensor=false'
        GEOCODE_START_REQUEST_URL = GEOCODE_START_REQUEST_URL.replace (" ", "%20")
        response_start_geocode_data = urllib2.urlopen(GEOCODE_START_REQUEST_URL).read()
        start_location_data = json.loads(response_start_geocode_data)
        lat_start = start_location_data["results"][0]["geometry"]["location"]["lat"]
        lng_start = start_location_data["results"][0]["geometry"]["location"]["lng"]
    if request.POST.get('EndingLocation'):
        GEOCODE_DEST_REQUEST_URL = 'http://maps.google.com/maps/api/geocode/json?address='+request.POST.get('Destination', False).encode('utf8')+'&sensor=false'
        GEOCODE_DEST_REQUEST_URL = GEOCODE_DEST_REQUEST_URL.replace (" ", "%20")
        response_dest_geocode_data = urllib2.urlopen(GEOCODE_DEST_REQUEST_URL).read()
        dest_location_data = json.loads(response_dest_geocode_data)
        lat_end = dest_location_data["results"][0]["geometry"]["location"]["lat"]
        lng_end = dest_location_data["results"][0]["geometry"]["location"]["lng"]

    start_location = {
        "lat" : lat_start,
        "lng" : lng_start,
    }

    end_location = {
        "lat" : lat_end,
        "lng" : lng_end,
    }

    current_user_fb_id = request.POST.get('search_form_fb_id', False).encode('utf8')

    for giver in all_givers:
        hyp_from_start = calc_hypotenuse(float(lat_start), float(lng_start), float(giver.lat_start), float(giver.lng_start))
        hyp_from_dest = calc_hypotenuse(float(lat_end), float(lng_end), float(giver.lat_end), float(giver.lng_end))
        if hyp_from_start <= MAX_RADIUS and hyp_from_dest <= MAX_RADIUS and (giver.fb_id != current_user_fb_id):
            request_url = GRAPH_API_BASE_URL+giver.fb_id.encode('utf8')
            response = urllib2.urlopen(request_url)
            response_data = response.read()
            data = json.loads(response_data)

            rating = 50*(hyp_from_start/MAX_RADIUS) + 50*(hyp_from_dest/MAX_RADIUS)

            nearby_givers.append(giver)
            giver_fb_id.append(giver.fb_id)
            giver_names.append(data['first_name'] + " " + data['last_name'])
            giver_ratings.append(rating)
            giver_lat_start.append(giver.lat_start)
            giver_lat_end.append(giver.lat_end)
            giver_lng_start.append(giver.lng_start)
            giver_lng_end.append(giver.lng_end)


    tupleOfDicts = []
    dict = []
    count=0
    for obj in nearby_givers:
        dict = {
             "fb_id" : giver_fb_id[count].encode('utf8'),
             "name" : giver_names[count].encode('utf8'),
             "rating" : giver_ratings[count],
             "lat_start" : giver_lat_start[count].encode('utf8'),
             "lat_end" : giver_lat_end[count].encode('utf8'),
             "lng_start" : giver_lng_start[count].encode('utf8'),
             "lng_end" : giver_lng_end[count].encode('utf8')
         }
        tupleOfDicts.append(dict)
        count += 1

    dump = json.dumps(tupleOfDicts)

    #dump = json.dumps(givers_zip_ratings)
    #dump = json.dumps('[["545547692", 86.4365540305593], ["592257540", 71.67730794690695], ["733050239", 75.02406966663716], ["100002131130870", 83.35098178107881], ["1645560180", 91.70583373342106], ["715076506", 75.73249881179504], ["517765107", 37.01613186970565], ["10204097819428052", 37.089990452084265]]')
    #dump = '[[{"fb_id": "545547692","rating": 86.4365540305593}],[{"fb_id": "592257540","rating": 71.67730794690695}],[{"fb_id": "733050239","rating": 75.02406966663716}],[{"fb_id": "100002131130870","rating": 83.35098178107881}],[{"fb_id": "1645560180","rating": 91.70583373342106}],[{"fb_id": "715076506","rating": 75.73249881179504}],[{"fb_id": "517765107","rating": 37.01613186970565}],[{"fb_id": "10204097819428052","rating": 37.089990452084265}]]'
    start_lat = start_location["lat"]
    start_lng = start_location["lng"]
    end_lat = start_location["lat"]
    end_lng = start_location["lng"]
    return render(request, 'index.html', { "start_lat" : start_lat,  "start_lng" : start_lng,  "end_lat" : end_lat, "end_lng" : end_lng, "dump" : dump})


def post_user(request):
    userID = request.POST.get('fb_id', False).encode('utf8')
    request_url = 'https://graph.facebook.com/me?access_token='+request.POST.get('accessToken', False).encode('utf8')
    response = urllib2.urlopen(request_url)
    response_data = response.read()
    data = json.loads(response_data)
    fbID = data['id'].encode('utf8')

    obj = Giver.objects.filter(fb_id=userID)
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