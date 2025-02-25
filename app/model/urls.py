from django.urls import path
from . import views

# http://127.0.0.1:8000/model/...
app_name='model'
urlpatterns = [
    path('', views.ModelCreateView.as_view(), name='model_create'),
    path('result', views.ModelResultView.as_view(), name='model_result'),
    path('movies', views.ModelMoviesView.as_view(), name='model_movies'),
    path('movies/<int:pk>', views.MovieDetailView.as_view(), name='movie_detail'),
    path('rate_movie/<int:movie_id>/<int:rating>/', views.rate_movie, name='rate_movie'),
]
