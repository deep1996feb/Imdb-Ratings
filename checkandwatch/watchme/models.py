from enum import auto
from django.db import models
from django.forms import IntegerField
from django .core .validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.
#old models
# class Movies(models.Model):
#     name = models.CharField(max_length=50, blank=True, default='')
#     description = models.CharField(max_length=200)
#     active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name

# New Models

class StreamPlatform(models.Model):
    name = models.CharField(max_length=100)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=50)

    def __str__(self):
        return self.name

class Watch_List(models.Model):
    Title = models.CharField(max_length=100)
    Description = models.CharField(max_length=200)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name='watchlist') #This line is used when we want create a relationship between two tables.
    active = models.BooleanField(default=True)
    avg_rating = models.FloatField(default=0)
    number_ratings = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.Title

class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    ratings = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200)
    watchlist = models.ForeignKey(Watch_List, on_delete=models.CASCADE, related_name='reviews')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.ratings) + "  |  " + self.watchlist.Title