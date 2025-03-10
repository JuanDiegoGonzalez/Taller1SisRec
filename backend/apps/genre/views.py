from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from .models import Genre
from backend.apps.movie_rating.models import MovieRating

class ModelGenresView(View):
    def get(self, request, genre_id):
        # Validate if the genre exists
        genre = get_object_or_404(Genre, id=genre_id)

        # Query from the Movie side to get all movies linked to the genre
        movies = MovieRating.objects.filter(genres__id=genre_id).values("id", "title", "imdb_url")

        # Pagination
        paginator = Paginator(movies, 10)  # 10 movies per page
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        data = {
            "genre": {"id": genre.id, "name": genre.name},
            "items": list(page_obj.object_list),
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "current_page": page_obj.number,
            "total_pages": paginator.num_pages,
        }

        return JsonResponse(data)
