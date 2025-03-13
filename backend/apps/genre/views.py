from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Genre

class ModelGenresView(View):
    def get(self, request, genre_id):
        # Validate if the genre exists
        genre = Genre.objects.filter(id=genre_id).first()

        if not genre:
            return JsonResponse({"error": "Genre not found"}, status=404)

        movies = genre.movies.all().order_by("id")

        # Pagination
        paginator = Paginator(movies, 10)  # 10 movies per page
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # Serialize movie data (adjust fields as needed)
        items = [
            {
                "id": movie.id,
                "title": movie.title,
                "image_url": movie.image_url,
                "avg_rating": movie.avg_rating,
            }
            for movie in page_obj.object_list
        ]

        # Response data
        data = {
            "genre": {"id": genre.id, "name": genre.name},
            "items": items,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "current_page": page_obj.number,
            "total_pages": paginator.num_pages,
        }

        return JsonResponse(data, safe=False)
