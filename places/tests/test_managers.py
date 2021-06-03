from places.managers import GoogleApi
from django.test import TestCase
from .constants import RESULTS, SIMPLIFIED_DICTS


class TestGoogleApi(TestCase):
    def setUp(self):
        self.googleApi = GoogleApi()

    def test_get_cards_dict_returns_undetailed_place_dict(self):
        result = self.googleApi.get_cards_dict(RESULTS)
        self.assertEqual(result, SIMPLIFIED_DICTS)
