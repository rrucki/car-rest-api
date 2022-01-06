from django.test import SimpleTestCase
from django.urls import reverse, resolve
from cars_rest_api.views import car_list, car_detail, rating, popularity


class TestUrls(SimpleTestCase):
    def test_cars_url_resolves(self):
        url = reverse('cars')
        self.assertEquals(resolve(url).func, car_list)

    def test_delete_url_resolves(self):
        url = reverse('delete', args=['1'])
        self.assertEquals(resolve(url).func, car_detail)

    def test_rating_url_resolves(self):
        url = reverse('rate')
        self.assertEquals(resolve(url).func, rating)

    def test_popularity_url_resolves(self):
        url = reverse('popular')
        self.assertEquals(resolve(url).func, popularity)
