from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator

import requests
import json
import environ

from .constants import PLACES

from accounts.models import Favorite

env = environ.Env()
environ.Env.read_env()


def index(request):
    """View function for home page of site."""
    return render(request, "index.html")

def get_results_from_google_place(request):
    """ Call Google APIs"""
    query_address = request.GET.get("q")
    query_type = request.GET['type']
    query_distance = request.GET['distance']


    address_payload = {
        "input": "{}".format(query_address),
        "inputtype": "textquery",
        "fields": "formatted_address,geometry,name",
        "key": env('GOOGLE_KEY')
    }

    address_response = requests.get(
        "https://maps.googleapis.com/maps/api/place/findplacefromtext/json",
        params=address_payload,
    )


    if address_response.status_code == 200:
        data = address_response.json()
        coordonnates = data['candidates'][0]['geometry']['location']

        nearby_payload = {
            "location": f"{coordonnates['lat']},{coordonnates['lng']}",
            "radius": query_distance,
            "type":query_type,
            "key": env('GOOGLE_KEY')
        }    

        nearby_response = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json",
            params=nearby_payload)

        nearby_response_json = nearby_response.json()
        google_results = nearby_response_json['results']

        results = []

        for google_result in google_results:
            if google_result.get('opening_hours') and google_result.get('vicinity') and google_result.get('rating'):
                result = {}
                result['place_id'] = google_result['place_id']
                result['name'] = google_result['name']
                result['address'] = google_result['vicinity']
                result['is_open'] = google_result['opening_hours']['open_now']
                results.append(result)
       
        
        context = {
            'results' : results,
            'address' : query_address,
            'type': PLACES[query_type],
            'distance': query_distance

            }
            

#### GERER L'ERREUR

    ## if status = ZERO_RESULTS faire quelque chose

        return render(request, "places/results.html", context=context)

def get_place_details(request):
    place_id = request.GET.get("id")

    payload = {
        'placeid': place_id,
        'key': env('GOOGLE_KEY')}
    response = requests.get("https://maps.googleapis.com/maps/api/place/details/json",
            params=payload)

    response_json = response.json()['result']

    place = {}
    place['id'] = place_id
    place['name'] = response_json['name']
    place['address'] = response_json['formatted_address']
    place['phone'] = response_json['formatted_phone_number']
    place['is_open'] = response_json['opening_hours']['open_now']
    place['opening_hours'] = response_json['opening_hours']['periods']
    place['types'] = response_json['types']

    if Favorite.objects.filter(
        user_id=request.user.id,
        place=place_id).exists():
        place['is_favorite'] = True
    else:
        place['is_favorite'] = False    

    context = {'place': place}
    return render(request, "places/place_details.html", context=context)

def manage_favorites(request):
    if request.method == 'POST' and request.is_ajax:
        place = request.POST.get('place_id')
        if Favorite.objects.filter(
            user_id=request.user.id, 
            place=place).exists():
            favorite = Favorite.objects.get(
                user_id=request.user.id, 
                place=place)
            Favorite.objects.filter(id=favorite.id).delete()
        else:    
            Favorite.objects.create(
                user_id=request.user.id,
                place=place
                ) 
    return render(request, "places/place_details.html")     

