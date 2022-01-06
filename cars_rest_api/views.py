from django.db.models import Avg
from django.contrib.sites import requests
from .models import Car, Rating
from .serializers import CarRatingSerializer, CarPopularitySerializer
from .serializers import RatingSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests


@api_view(['GET', 'POST'])
def car_list(request):
    if request.method == 'GET':
        cars = Car.objects.all()
        serializer = CarRatingSerializer(cars, many=True)
        for car in serializer.data:
            ratings_filtered = Rating.objects.filter(car_id=car['id'])
            ratings_avg = ratings_filtered.aggregate(Avg('rating'))
            car['avg_rating'] = ratings_avg['rating__avg']
        return Response(serializer.data)

    elif request.method == 'POST':
        response = requests.get(
            'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/'
            '{}?format=json'.format(request.data['make']))
        response = response.json()
        for model in response['Results']:
            if model['Model_Name'] == request.data['model']:
                serializer = CarRatingSerializer(data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED)
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(request.data, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET', 'DELETE'])
def car_detail(request, pk):
    try:
        car = Car.objects.get(pk=pk)
    except Car.DoesNotExist:
        return Response(request.data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        car = Car.objects.get(pk=pk)
        serializer = CarRatingSerializer(car)
        return Response(serializer.data)

    if request.method == 'DELETE':
        car.delete()
        return Response(request.data, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def rating(request):
    if request.method == 'POST':
        try:
            Car.objects.get(pk=request.data['car_id'])
        except Car.DoesNotExist:
            return Response(request.data, status=status.HTTP_404_NOT_FOUND)
        serializer = RatingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def popularity(request):
    cars = Car.objects.all()

    for car in cars:
        ratings_filtered = Rating.objects.filter(car_id=car.id).count()
        car.rates_number = ratings_filtered
        car.save()

    cars = Car.objects.order_by('-rates_number')
    serializer = CarPopularitySerializer(cars, many=True)
    return Response(serializer.data)
