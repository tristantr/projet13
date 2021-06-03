import requests
import json
import environ

from accounts.models import Favorite, Comment

class GoogleApi:
    def __init__(self):
        self.env = environ.Env()
        environ.Env.read_env()

    def get_cards_dict(self, results):
        """ Get simplified dict for cards """
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

    def get_place_dict(self, place_id, user_id):
        """ Generate custom dict with place details """
        payload = {
            'placeid': place_id,
            'key': self.env('GOOGLE_KEY')}
        response = requests.get("https://maps.googleapis.com/maps/api/place/details/json",
                params=payload)

        response_json = response.json()['result']           

        place = {}
        place['id'] = place_id
        place['name'] = response_json['name']
        place['coordonates'] = response_json['geometry']['location']
        place['address'] = response_json['formatted_address']
        place['phone'] = response_json.get('formatted_phone_number', 'Non connu')
        place['is_open'] = response_json['opening_hours']['open_now']
        unformatted_hours = response_json['opening_hours']['weekday_text']
        place['opening_hours'] = self.format_datetime(unformatted_hours)
        place['types'] = response_json['types']
        place['reviews'] = response_json['reviews']

        comments = Comment.objects.filter(place=place_id)
        formatted_comments = []
        for comment in comments:
            formatted_comment = comment.get_comment()
            formatted_comments.append(formatted_comment)

        place['comments'] = formatted_comments

        if Favorite.objects.filter(
            user_id=user_id,
            place=place_id).exists():
            place['is_favorite'] = True
        else:
            place['is_favorite'] = False
        return place 

    def format_datetime(self, datetime):
        opening_hours = []
        for string in datetime:
            day = {}
            datetime = string.split(": ")
            day['day'] = datetime[0]
            day['hours'] = datetime[1]
            opening_hours.append(day)
        return opening_hours   


    def get_place(self, address):
        """ Find a place coordonates using text input """
        payload = {
            "input": "{}".format(address),
            "inputtype": "textquery",
            "fields": "formatted_address,geometry,name",
            "key": self.env('GOOGLE_KEY')
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

    def get_nearby_places(self, coordonates, distance, type):
        """ Find nearby places using coordonates, distance, dans place type """
        payload = {
            "location": f"{coordonates['lat']},{coordonates['lng']}",
            "radius": distance,
            "type":type,
            "key": self.env('GOOGLE_KEY')
        }    

        response = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json",
            params=payload)

        response_json = response.json()
        results = response_json['results']

        return results