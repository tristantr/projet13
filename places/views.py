from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import CreateView

from .managers import GoogleApi
from .forms import CommentForm

import requests
import json
import environ
import ast
from datetime import datetime

from .constants import PLACES

from accounts.models import Favorite, Comment, User
from django.contrib.auth.decorators import login_required


env = environ.Env()
environ.Env.read_env()

google_api = GoogleApi()

def index(request):
    """ Go to home page """
    return render(request, "index.html")

def get_places(request):
    """ Get places using various google api calls """
    address = request.GET.get("q")
    type = request.GET['type']
    distance = request.GET['distance']
    coordonates = google_api.get_place(address)

    if coordonates:
        results = google_api.get_nearby_places(coordonates, distance, type)
        places = google_api.get_cards_dict(results)
             
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
    place = google_api.get_place_dict(place_id, request.user.id)

    context = {
        'place': place, 
        'my_lat': coordonates['lat'],
        'my_lng': coordonates['lng']
        }

    return render(request, "places/place_details.html", context=context)

@login_required
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

@login_required
def get_favorites(request):
    """ Display favorites """
    user = request.user.id
    favorites = Favorite.objects.filter(user_id=user)
    places = []

    for favorite in favorites:
        place = google_api.get_place_dict(place_id=favorite.place, user_id=user)
        places.append(place)

    context = {'places': places}    

    return render(request, "places/favorites.html", context=context)

@login_required
def add_comment(request):
    """ Add a comment for a selected place """
    place = google_api.get_place_dict(request.GET.get("id"), request.user.id)

    form = CommentForm()
    if request.method == "POST":
        Comment.objects.create(
            place=request.POST.get("id"),
            user=User.objects.get(id=request.user.id),
            body=request.POST.get("body")
            )
        place = google_api.get_place_dict(request.POST.get("id"), request.user.id)

        context={'place': place,
                'my_lat': request.GET.get("lat"),
                'my_lng': request.GET.get("lng")}
        return render(request, 'places/place_details.html', context=context)

    context = {"form": form, 'place': place}    
    return render(request, "places/add_comment.html", context=context)


    