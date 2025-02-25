from django.shortcuts import render
from django.views.generic.edit import CreateView

from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.paginator import Paginator

from model.forms import CreateForm
from model.process import proceso

import time
import pandas as pd

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

class ModelCreateView(LoginRequiredMixin, CreateView):
    template_name = 'model/model_form.html'
    success_url = reverse_lazy('model:model_result')

    def get(self, request):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})
        
        model = form.save(commit=False)
        model.owner = request.user

        start_time = time.time()  # Start timer
        predicciones = proceso(model.modelo, model.tipo, model.k, int(model.owner.username))
        end_time = time.time()  # End timer
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.4f} seconds")
        
        predicciones_json = predicciones.to_dict(orient='records')

        request.session['predicciones'] = predicciones_json
        return redirect(self.success_url)

class ModelResultView(View):
    template_name = "model/model_result.html"

    def get(self, request) :
        context = {'predicciones' : request.session['predicciones']}
        return render(request, self.template_name, context)
    
class ModelMoviesView(View):
    template_name = "model/model_movies.html"

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

        # TODO: Cambiar y seleccionar columnas, o hacer detail de cada película
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

class MovieDetailView(View):
    template_name = "model/movie_detail.html"

    def get(self, request, pk) :
        items=pd.read_csv('../Dataset 100k/u.item', engine ='python', sep = '\|', names = ['movie_id' ,'movie_title','release_date','video release date','imdb_url','unknown',
                                                'Action','Adventure','Animation','Children','Comedy','Crime','Documentary','Drama',
                                                'Fantasy','Film_Noir','Horror','Musical','Mystery','Romance','Sci_Fi','Thriller','War','Western'], encoding='latin-1' )

        movie = items[items["movie_id"] == pk]
        movie_json = movie.to_dict(orient='records')

        print(movie_json)

        context = { 'movie' : movie_json[0]}
        return render(request, self.template_name, context)

@csrf_exempt
# TODO
def rate_movie(request, movie_id, rating):
    if request.method == 'POST' and request.user.is_authenticated:
        # Aquí debes guardar la calificación en la base de datos
        print(f'Usuario {request.user} calificó la película {movie_id} con {rating} estrellas.')
        
        # Suponiendo que tienes un modelo MovieRating:
        # MovieRating.objects.update_or_create(user=request.user, movie_id=movie_id, defaults={'rating': rating})

        return JsonResponse({'message': 'Calificación registrada con éxito'}, status=200)
    
    return JsonResponse({'error': 'No autorizado'}, status=403)
