from django.urls import path
from . import views

# http://127.0.0.1:8000/movies/...
app_name='movies'
urlpatterns = [
    path('', views.ModelMoviesView.as_view(), name='movie_list'),
    path('<int:pk>', views.MovieDetailView.as_view(), name='movie_detail'),
    path('rate_movie/<int:movie_id>/<int:rating>/', views.rate_movie, name='rate_movie'),
]
