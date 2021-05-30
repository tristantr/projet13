from django.shortcuts import render
from django.http import HttpResponseRedirect

from .managers import get_place_dict, find_place_with_google_api, find_nearby_places_with_google_api

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

def get_places(request):
    """ Call Google APIs"""
    address = request.GET.get("q")
    type = request.GET['type']
    distance = request.GET['distance']
    coordonates = find_place_with_google_api(address)

    if coordonates:
        results = find_nearby_places_with_google_api(coordonates, distance, type)
        places = []

        for result in results:
            if result.get('opening_hours') and result.get('vicinity'):
                place = {}
                place['id'] = result['place_id']
                place['name'] = result['name']
                place['address'] = result['vicinity']
                place['is_open'] = result['opening_hours']['open_now']
                places.append(place)
             
        context = {
            'places' : places,
            'address' :address,
            'type': PLACES[type],
            'distance': distance
            }
        return render(request, "places/results.html", context=context)
    else:
        context = { 'places' : []}
        return render(request, "places/results.html", context=context)   
            

#### GERER L'ERREUR

    ## if status = ZERO_RESULTS faire quelque chose


def get_place_details(request):
    place_id = request.GET.get("id")
    print(place_id)
    place = get_place_dict(place_id=place_id, user_id=request.user.id)    

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
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

def get_favorites(request):
    user = request.user.id
    favorites = Favorite.objects.filter(user_id=user)
    places = []

    for favorite in favorites:
        place = get_place_dict(place_id=favorite.place, user_id=user)
        places.append(place)

    context = {'places': places}    

    return render(request, "places/favorites.html", context=context)


