from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from django.contrib import auth



class HomePageView(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, "index.html")



class FavoritesView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.credentials = {"email": "products@gmail.com",
                            "pseudo": "pseudo",
                            "password": "password"}
        cls.user = User.objects.create_user("products@gmail.com", "pseudo", "password")

    def setUp(self):
        self.client.post(reverse("login"), self.credentials)
        self.client_user = auth.get_user(self.client)

    def test_get_favorites(self):
        """Test that the logged user can access favorites"""
        response = self.client.get(reverse("get_favorites"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "places/favorites.html")

### Uncomment the following tests and use your own Google Key 

# class PlaceView(TestCase):
#     def test_get_search_result(self):
#         """ Test the search section """
#         response = self.client.get(reverse("search_results"),{
#             'q': '30 Avenue Daumesnil, Paris, France',
#             'type': 'bakery',
#             'distance': 400
#             })
#         self.assertEqual(response.status_code, 200)    
#         self.assertTemplateUsed(response, "places/results.html")


#     def test_get_place_details(self):
#         """ Test that the get method to access a product details works well"""
#         response = self.client.get(reverse("place_details"), {
#             'id': 'ChIJXYCkv2dt5kcRZs2yU8Iyx9U',
#             'coordonates': "{'lat': 48.865794, 'lng': 2.4415082}"}
#             )
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "places/place_details.html")    