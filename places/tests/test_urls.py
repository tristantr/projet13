from django.test import SimpleTestCase
from django.urls import resolve, reverse
from places import views


class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        url = reverse("index")
        self.assertEquals(resolve(url).func, views.index)

    def test_search_url_is_resolved(self):
        url = reverse("search_results")
        self.assertEquals(resolve(url).func, views.get_places)

    def test_get_favorites_url_is_resolved(self):
        url = reverse("get_favorites")
        self.assertEquals(resolve(url).func, views.get_favorites)

    def test_manage_favorites_url_is_resolved(self):
        url = reverse("manage_favorites")
        self.assertEquals(resolve(url).func, views.manage_favorites)

    def test_get_place_details_url_is_resolved(self):
        url = reverse("place_details")
        self.assertEquals(resolve(url).func, views.get_place_details) 

    def test_add_comment_url_is_resolved(self):
        url = reverse("add_comment")
        self.assertEquals(resolve(url).func, views.add_comment)