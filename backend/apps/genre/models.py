from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.movie.models import Movie

class Genre(models.Model):
    name = models.CharField(max_length=255)
    movies = models.ManyToManyField(Movie)

    def __str__(self):
        return self.name