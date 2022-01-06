from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    avg_rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    rates_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '%s %s' % (self.make, self.model)


class Rating(models.Model):
    car_id = models.PositiveIntegerField(default=0)
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)

    def __str__(self):
        return self.car_id
