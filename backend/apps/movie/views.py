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
from apps.movie_rating.models import MovieRating

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
            # Si el usuario está en el dataframe
            try:
                user_id = int(request.user.username)

                ratings=pd.read_csv('../Dataset 100k/u.data', engine ='python', sep = '\t', names = ['user_id', 'movie_id', 'rating', 'timestamp'])
                user_ratings = ratings[ratings["user_id"] == user_id][["movie_id", "rating"]]

            # Si es un nuevo usuario
            except:
                ratings = MovieRating.objects.filter(user=request.user).values('movie_id', 'rating')
                if ratings.exists():
                    user_ratings = pd.DataFrame(list(ratings))
                else:
                    user_ratings = pd.DataFrame(columns=['movie_id', 'rating'])
                user_ratings.insert(0, 'user_id', request.user.username)
                print(user_ratings)

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
            # Si el usuario está en el dataframe
            try:
                user_id = int(request.user.username)

                ratings=pd.read_csv('../Dataset 100k/u.data', engine ='python', sep = '\t', names = ['user_id', 'movie_id', 'rating', 'timestamp'])
                user_ratings = ratings[ratings["user_id"] == user_id][["movie_id", "rating"]]
            # Si es un nuevo usuario
            except:
                ratings = MovieRating.objects.filter(user=request.user).values('movie_id', 'rating')
                if ratings.exists():
                    user_ratings = pd.DataFrame(list(ratings))
                else:
                    user_ratings = pd.DataFrame(columns=['movie_id', 'rating'])
                user_ratings.insert(0, 'user_id', request.user.username)
                print(user_ratings)

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

@api_view(['GET'])
def api_movie_list(request):
    strval = request.GET.get("search", False)
    filter_rated = request.GET.get("filter_rated", False)
    genre_id = request.GET.get("genre", False)

    from .models import Movie
    from apps.genre.models import Genre
    
    # Get movies from database
    movies = Movie.objects.all()
    
    # Filter by genre if provided
    if genre_id:
        try:
            genre = Genre.objects.get(id=genre_id)
            movies = genre.movies.all()
        except Genre.DoesNotExist:
            pass
    
    # Filter by search term
    if strval:
        movies = movies.filter(title__icontains=strval)
    
    # Filter by user rating
    if request.user.is_authenticated and filter_rated:
        # Get only movies rated by the user
        user_ratings = MovieRating.objects.filter(user=request.user, rating__gt=0).values_list('movie_id', flat=True)
        movies = movies.filter(id__in=user_ratings)

    # Prepare response data
    movies_data = []
    
    for movie in movies:
        movie_data = {
            "movie_id": movie.id,
            "movie_title": movie.title,
            "imdb_url": movie.image_url,
            "avg_rating": movie.avg_rating
        }
        
        # Add rating if user is authenticated
        if request.user.is_authenticated:
            try:
                rating = MovieRating.objects.get(user=request.user, movie=movie).rating
            except MovieRating.DoesNotExist:
                rating = 0
            movie_data["rating"] = rating
            
        movies_data.append(movie_data)

    # Paginate results
    paginator = Paginator(movies_data, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    data = {
        "items": page_obj.object_list,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
        "current_page": page_obj.number,
        "total_pages": paginator.num_pages,
    }
    
    return Response(data)
