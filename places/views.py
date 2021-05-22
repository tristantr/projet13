from django.shortcuts import render
from django.views import generic

import requests
import json
import environ

env = environ.Env()
environ.Env.read_env()


def index(request):
    """View function for home page of site."""
    return render(request, "index.html")

def get_results_from_google_place(request):
    query = request.GET.get("q")
    restaurants = request.GET.get("restaurants")
    supermarkets = request.GET.get("supermarkets")
    bakeries = request.GET.get("bakeries")

    print(restaurants, supermarkets, bakeries)

    payload = {
        "input": "{}".format(query),
        "inputtype": "textquery",
        "fields": "formatted_address,geometry,name",
        "key": env('GOOGLE_KEY')
    }

    response = requests.get(
        "https://maps.googleapis.com/maps/api/place/findplacefromtext/json",
        params=payload,
    )

    if response.status_code == 200:
        data = response.json()

    print(data)

    ## if status = ZERO_RESULTS faire quelque chose 

    return render(request, "index.html")