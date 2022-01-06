from rest_framework import serializers
from .models import Car, Rating


class CarRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'avg_rating']


class CarPopularitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'rates_number']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['car_id', 'rating']
