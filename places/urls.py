from django.urls import path
from . import views

urlpatterns = [
	path("", views.index, name="index"),

	path("search/", views.get_results_from_google_place, name="search_results"),

	path("places/", views.get_place_details, name="place_details"),

	path("places/favorites/", views.manage_favorites, name="manage_favorites")
]