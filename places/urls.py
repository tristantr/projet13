from django.urls import path
from . import views

urlpatterns = [
	path("", views.index, name="index"),

	path("search/", views.get_places, name="search_results"),

	path("places/", views.get_place_details, name="place_details"),

	path("places/favorites/", views.manage_favorites, name="manage_favorites"),

	path("places/my_favorites/", views.get_favorites, name="get_favorites")

]