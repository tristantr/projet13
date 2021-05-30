from django.shortcuts import render
from django.http import HttpResponseRedirect

from .managers import get_place_dict, find_place_with_google_api, find_nearby_places_with_google_api

import requests
import json
import environ
import ast

from .constants import PLACES

from accounts.models import Favorite

env = environ.Env()
environ.Env.read_env()


def index(request):
    """ Go to home page """
    return render(request, "index.html")

def get_places(request):
    """ Get places using various google api calls """
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
            'coordonates': coordonates,
            'places' : places,
            'address' :address,
            'type': PLACES[type],
            'distance': distance
            }
        return render(request, "places/results.html", context=context)
    else:
        context = { 'places' : []}
        return render(request, "places/results.html", context=context)   


def get_place_details(request):
    """ Get details of a specific place """
    place_id = request.GET.get("id")
    coordonates = ast.literal_eval(request.GET.get("coordonates"))
    place = get_place_dict(place_id, request.user.id)    

    context = {
        'place': place, 
        'my_lat': coordonates['lat'],
        'my_lng': coordonates['lng']
        }

    return render(request, "places/place_details.html", context=context)

def manage_favorites(request):
    """ Handle favorite section"""
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
    """ Display favorites """
    user = request.user.id
    favorites = Favorite.objects.filter(user_id=user)
    places = []

    for favorite in favorites:
        place = get_place_dict(place_id=favorite.place, user_id=user)
        places.append(place)

    context = {'places': places}    

    return render(request, "places/favorites.html", context=context)


