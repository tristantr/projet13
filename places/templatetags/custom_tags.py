from django import template
from django.template.loader import get_template

register = template.Library()


def display_place(place, coordonates=None):
    return {"place": place, "coordonates": coordonates}

place_template = get_template("places/place.html")
register.inclusion_tag(place_template)(display_place)
