from django.shortcuts import render

from django.views import View
from django.shortcuts import render

from django.core.paginator import Paginator

import pandas as pd

from django.http import JsonResponse

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MovieRating
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import json

#-------------------------------------
# Nuevos endpoints
#-------------------------------------
@method_decorator(csrf_exempt, name="dispatch")
class MovieRateView(View):
    def post(self, request, movie_id):
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            rating = data.get("rating")

            print(f'Usuario {user_id} calificó la película {movie_id} con {rating} estrellas.')
            MovieRating.objects.update_or_create(user_id=user_id, movie_id=movie_id, defaults={'rating': rating})

            return JsonResponse({"success": "Movie rated succesfully"}, safe=False)

        except json.JSONDecodeError:

            return JsonResponse({"error": "Invalid JSON"}, status=400)

@method_decorator(csrf_exempt, name="dispatch")
class MovieUserRatingView(View):
    def get(self, request):
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            user_ratings = MovieRating.objects.filter(user_id=user_id).select_related('movie')

            if not user_ratings.exists():
                return JsonResponse({"error": f"No movies found for user {user_id}"}, status=404)

            movies_info = [
                {
                    "id": rating.movie.id,
                    "title": rating.movie.title,
                    "image_url": rating.movie.image_url,
                    "user_rating": rating.rating
                }
                for rating in user_ratings
            ]

            return JsonResponse({"user_id": user_id, "movies": movies_info}, safe=False)

        except json.JSONDecodeError:

            return JsonResponse({"error": "Invalid JSON"}, status=400)
