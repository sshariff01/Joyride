from django.shortcuts import render, render_to_response
from givers.models import Giver
from math import sin, cos, radians, degrees, acos, sqrt
import json
import urllib2

GRAPH_API_BASE_URL = 'https://graph.facebook.com/'
MAX_RADIUS = 0.11

def index(request):
    start_lat="43.722598"
    start_lng="-79.645825"
    data = { "start_lat" : start_lat,  "start_lng" : start_lng}
    return render(request, 'index.html', data)

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
    giver_distance_start_positions = []

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

            rating = calc_rating(hyp_from_start, hyp_from_dest)

            nearby_givers.append(giver)
            giver_fb_id.append(giver.fb_id)
            giver_names.append(data['first_name'] + " " + data['last_name'])
            giver_ratings.append(rating)
            giver_lat_start.append(giver.lat_start)
            giver_lat_end.append(giver.lat_end)
            giver_lng_start.append(giver.lng_start)
            giver_lng_end.append(giver.lng_end)
            giver_distance_start_positions.append(get_duration(str(lat_start), str(lng_start), giver.lat_start, giver.lng_start))


    arrayOfDicts = []
    count=0

    #graph.facebook.com/me/13618575/picture?redirect=false

    for i in range(0, nearby_givers.__len__(), 1):
        dict = {
             "fb_id" : giver_fb_id[i].encode('utf8'),
             "fb_picture" : get_facebook_picture(giver_fb_id[i].encode('utf8')),
             "name" : giver_names[i].encode('utf8'),
             "rating" : round(giver_ratings[i], 1),
             "lat_start" : giver_lat_start[i].encode('utf8'),
             "lat_end" : giver_lat_end[i].encode('utf8'),
             "lng_start" : giver_lng_start[i].encode('utf8'),
             "lng_end" : giver_lng_end[i].encode('utf8'),
             "duration_from_start" : giver_distance_start_positions[i].encode('utf8')
         }
        arrayOfDicts.append(dict)
        count += 1

    sortedList = sorted(arrayOfDicts, key=lambda k: k['rating'], reverse=True)
    dump = json.dumps(sortedList[:5])

    start_lat = start_location["lat"]
    start_lng = start_location["lng"]
    end_lat = end_location["lat"]
    end_lng = end_location["lng"]
    data = { "start_lat" : start_lat,  "start_lng" : start_lng,  "end_lat" : end_lat, "end_lng" : end_lng, "dump" : dump}
    return render(request, 'index.html', data)

def get_facebook_picture(facebook_id):
    return "https://graph.facebook.com/v2.0/" + facebook_id + "/picture?type=large"
    # response = urllib2.urlopen(PICTURE_URL)
    # return response.url
    # response_data = response.read()
    # data = json.loads(response_data)
    # pictureUrl = data['data']['url']
    # return pictureUrl

def get_duration(lat_1, lng_1, lat_2, lng_2):
    GOOGLE_API_KEY = "AIzaSyDiqODRLvfieiM6iGbUR4Rk62YkKT7dqPw"
    response_data = urllib2.urlopen("https://maps.googleapis.com/maps/api/directions/json?origin="+lat_1+","+lng_1+"&destination="+lat_2+","+lng_2+"&key="+GOOGLE_API_KEY).read()
    data = json.loads(response_data)
    duration = data["routes"][0]["legs"][0]["duration"]["text"]
    return duration


def post_user(request):
    userID = request.POST.get('fb_id', False).encode('utf8')
    request_url = 'https://graph.facebook.com/me?access_token='+request.POST.get('accessToken', False).encode('utf8')
    response = urllib2.urlopen(request_url)
    response_data = response.read()
    data = json.loads(response_data)
    fbID = data['id'].encode('utf8')

    obj = Giver.objects.filter(fb_id = userID)
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

def calc_rating(hyp_from_start, hyp_from_dest):
    return 50*(hyp_from_start/MAX_RADIUS) + 50*(hyp_from_dest/MAX_RADIUS)

def profile(request):
    if request.GET.get('id', False):
        giver = Giver.objects.get(fb_id = request.GET.get('id', False))

        hyp_from_start = calc_hypotenuse(float(request.GET.get('start_lat')), float(request.GET.get('start_lng')), float(giver.lat_start), float(giver.lng_start))
        hyp_from_dest = calc_hypotenuse(float(request.GET.get('end_lat')), float(request.GET.get('end_lng')), float(giver.lat_end), float(giver.lng_end))

        fb_graph_url = GRAPH_API_BASE_URL+request.GET.get('id', False)
        response = urllib2.urlopen(fb_graph_url).read()
        response_data = json.loads(response)

        data = {
            "name" : response_data["first_name"] + " " + response_data["last_name"],
            "fb_img" : get_facebook_picture(request.GET.get('id', False)),
            "rating" : round(calc_rating(hyp_from_start, hyp_from_dest), 1),
            "distance" : get_duration(str(request.GET.get('start_lat')), str(request.GET.get('start_lng')), giver.lat_start, giver.lng_start)
        }
        return render(request, 'profile.html', data)