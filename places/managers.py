import requests
import json
import environ

from accounts.models import Favorite

env = environ.Env()
environ.Env.read_env()

def get_cards_dict(results):
    places = []
    for result in results:
        if result.get('opening_hours') and result.get('vicinity'):
            place = {}
            place['id'] = result['place_id']
            place['name'] = result['name']
            place['address'] = result['vicinity']
            place['is_open'] = result['opening_hours']['open_now']
            places.append(place)

    return places        



def get_place_dict(place_id, user_id):
    """ Generate custom dict with place details """
    payload = {
        'placeid': place_id,
        'key': env('GOOGLE_KEY')}
    response = requests.get("https://maps.googleapis.com/maps/api/place/details/json",
            params=payload)

    response_json = response.json()['result']

    place = {}
    place['id'] = place_id
    place['name'] = response_json['name']
    place['coordonates'] = response_json['geometry']['location']
    place['address'] = response_json['formatted_address']
    place['phone'] = response_json['formatted_phone_number']
    place['is_open'] = response_json['opening_hours']['open_now']
    place['opening_hours'] = response_json['opening_hours']['periods']
    place['types'] = response_json['types']

    if Favorite.objects.filter(
        user_id=user_id,
        place=place_id).exists():
        place['is_favorite'] = True
    else:
        place['is_favorite'] = False

    return place    

def get_place(address):
    """ Find a place coordonates using text input """
    payload = {
        "input": "{}".format(address),
        "inputtype": "textquery",
        "fields": "formatted_address,geometry,name",
        "key": env('GOOGLE_KEY')
    }

    response = requests.get(
        "https://maps.googleapis.com/maps/api/place/findplacefromtext/json",
        params=payload,
    )

    try:
        if response.status_code == 200:
            data = response.json()
            coordonates = data['candidates'][0]['geometry']['location']
    except:
        coordonates = []
        return coordonates      

    return coordonates

def get_nearby_places(coordonates, distance, type):
    """ Find nearby places using coordonates, distance, dans place type """
    payload = {
        "location": f"{coordonates['lat']},{coordonates['lng']}",
        "radius": distance,
        "type":type,
        "key": env('GOOGLE_KEY')
    }    

    response = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json",
        params=payload)

    response_json = response.json()
    results = response_json['results']

    return results







