from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    avg_rating = models.FloatField()

    def __str__(self):
        return f"Movie {self.id}: {self.title}"
