from rest_framework.test import APITestCase
from cars_rest_api.models import Car, Rating
import requests


class TestCar(APITestCase):
    url = "/cars/"

    def setUp(self):
        Car.objects.create(make="Volksvagen", model="Golf")
        Rating.objects.create(car_id=1, rating=4)
        Rating.objects.create(car_id=1, rating=2)

    def test_get_cars(self):
        response = self.client.get(self.url)
        result = response.json()

        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["make"], "Volksvagen")
        self.assertEqual(result[0]["model"], "Golf")
        self.assertEqual(result[0]["avg_rating"], 3)
        self.assertEqual(response.status_code, 200)

    def test_post_car(self):
        data = {
            "make": "Volkswagen",
            "model": "Golf"
        }
        response = self.client.post(self.url, data=data)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["make"], "Volkswagen")
        self.assertEqual(result["model"], "Golf")

        response = requests.get(
            'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/'
            '{}?format=json'.format(data['make']))
        response_external = response.json()

        model_checker = ""
        for model in response_external['Results']:
            if model['Model_Name'] == result['model']:
                model_checker = model['Model_Name']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["model"], model_checker)


class TestGetCarPopular(APITestCase):
    url = "/popular/"

    def setUp(self):
        Car.objects.create(make="Volksvagen", model="Golf")
        Rating.objects.create(car_id="1", rating="4")

    def test_get_cars(self):
        response = self.client.get(self.url)
        result = response.json()

        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["make"], "Volksvagen")
        self.assertEqual(result[0]["model"], "Golf")
        self.assertEqual(result[0]["rates_number"], 1)
        self.assertEqual(response.status_code, 200)


class TestGetRating(APITestCase):
    url = "/rate/"

    def setUp(self):
        Car.objects.create(make="Volksvagen", model="Golf")
        Rating.objects.create(car_id="1", rating="4")

    def test_post_rating(self):
        Car.objects.create(make="Volksvagen", model="Golf")
        data = {
            "car_id": 1,
            "rating": 4
        }
        response = self.client.post(self.url, data=data)
        result = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["car_id"], 1)
        self.assertEqual(result["rating"], 4)
