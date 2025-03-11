from django.db import models
from django.contrib.auth.models import User
from apps.movie.models import Movie

class MovieRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings")
    rating = models.FloatField()

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} - Movie {self.movie.id}: {self.rating}"
