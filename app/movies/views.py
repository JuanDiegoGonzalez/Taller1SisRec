from django.shortcuts import render

from django.views import View
from django.shortcuts import render

from django.core.paginator import Paginator

import pandas as pd

from django.http import JsonResponse

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

#-------------------------------------
# Nuevos endpoints
#-------------------------------------
class ModelMoviesView(View):
    template_name = "movies/movie_list.html"

    def get(self, request) :
        strval =  request.GET.get("search", False)
        filter_rated = request.GET.get("filter_rated", False)

        items=pd.read_csv('../Dataset 100k/u.item', engine ='python', sep = '\|', names = ['movie_id' ,'movie_title','release date','video release date','imdb_url','unknown',
                                                'Action','Adventure','Animation','Children','Comedy','Crime','Documentary','Drama',
                                                'Fantasy','Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western'], encoding='latin-1' )

        if request.user.is_authenticated:
            ratings=pd.read_csv('../Dataset 100k/u.data', engine ='python', sep = '\t', names = ['user_id', 'movie_id', 'rating', 'timestamp'])
            
            user_id = int(request.user.username)
            user_ratings = ratings[ratings["user_id"] == user_id][["movie_id", "rating"]]

            items = items.merge(user_ratings, on="movie_id", how="left")
            items["rating"].fillna(0, inplace=True)

            if filter_rated:
                items = items[items["rating"] > 0]
                strval = None
        
        if strval:
           items = items[items["movie_title"].str.contains(strval, case=False, na=False)]

        if request.user.is_authenticated:
            items_json = items[["movie_id", "movie_title", "imdb_url", "rating"]].to_dict(orient='records')
        else:
            items_json = items[["movie_id", "movie_title", "imdb_url"]].to_dict(orient='records')

        paginator = Paginator(items_json, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        print(page_obj.object_list)

        data = {
            "items": page_obj.object_list,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "current_page": page_obj.number,
            "total_pages": paginator.num_pages,
        }

        context = {'data' : data, 'search': strval, 'filter_rated': filter_rated}
        return JsonResponse(context)

class MovieDetailView(View):
    template_name = "movies/movie_detail.html"

    def get(self, request, pk) :
        items=pd.read_csv('../Dataset 100k/u.item', engine ='python', sep = '\|', names = ['movie_id' ,'movie_title','release_date','video release date','imdb_url','unknown',
                                                'Action','Adventure','Animation','Children','Comedy','Crime','Documentary','Drama',
                                                'Fantasy','Film_Noir','Horror','Musical','Mystery','Romance','Sci_Fi','Thriller','War','Western'], encoding='latin-1' )

        movie = items[items["movie_id"] == pk]
        movie_json = movie.to_dict(orient='records')

        print(movie_json)

        context = { 'movie' : movie_json[0]}
        return JsonResponse(context)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_movie(request, movie_id, rating):
    user = request.user  # Usuario autenticado

    # Aquí debes guardar la calificación en la base de datos
    print(f'Usuario {user} calificó la película {movie_id} con {rating} estrellas.')

    # Ejemplo con un modelo MovieRating
    # MovieRating.objects.update_or_create(user=user, movie_id=movie_id, defaults={'rating': rating})

    return Response({'message': 'Calificación registrada con éxito'}, status=200)

#-------------------------------------
# Anteriores endpoints
#-------------------------------------
class ModelOldMoviesView(View):
    template_name = "movies/movie_list.html"

    def get(self, request) :
        strval =  request.GET.get("search", False)
        filter_rated = request.GET.get("filter_rated", False)

        items=pd.read_csv('../Dataset 100k/u.item', engine ='python', sep = '\|', names = ['movie_id' ,'movie_title','release date','video release date','imdb_url','unknown',
                                                'Action','Adventure','Animation','Children','Comedy','Crime','Documentary','Drama',
                                                'Fantasy','Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western'], encoding='latin-1' )

        if request.user.is_authenticated:
            ratings=pd.read_csv('../Dataset 100k/u.data', engine ='python', sep = '\t', names = ['user_id', 'movie_id', 'rating', 'timestamp'])
            
            user_id = int(request.user.username)
            user_ratings = ratings[ratings["user_id"] == user_id][["movie_id", "rating"]]

            items = items.merge(user_ratings, on="movie_id", how="left")
            items["rating"].fillna(0, inplace=True)

            if filter_rated:
                items = items[items["rating"] > 0]
                strval = None
        
        if strval:
           items = items[items["movie_title"].str.contains(strval, case=False, na=False)]

        if request.user.is_authenticated:
            items_json = items[["movie_id", "movie_title", "imdb_url", "rating"]].to_dict(orient='records')
        else:
            items_json = items[["movie_id", "movie_title", "imdb_url"]].to_dict(orient='records')

        paginator = Paginator(items_json, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        print(page_obj.object_list)

        context = {'page_obj' : page_obj, 'search': strval, 'filter_rated': filter_rated}
        return render(request, self.template_name, context)

class MovieOldDetailView(View):
    template_name = "movies/movie_detail.html"

    def get(self, request, pk) :
        items=pd.read_csv('../Dataset 100k/u.item', engine ='python', sep = '\|', names = ['movie_id' ,'movie_title','release_date','video release date','imdb_url','unknown',
                                                'Action','Adventure','Animation','Children','Comedy','Crime','Documentary','Drama',
                                                'Fantasy','Film_Noir','Horror','Musical','Mystery','Romance','Sci_Fi','Thriller','War','Western'], encoding='latin-1' )

        movie = items[items["movie_id"] == pk]
        movie_json = movie.to_dict(orient='records')

        print(movie_json)

        context = { 'movie' : movie_json[0]}
        return render(request, self.template_name, context)
