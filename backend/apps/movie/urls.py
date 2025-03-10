from django.urls import path
from . import views

# http://127.0.0.1:8000/movies/...
app_name='movie'
urlpatterns = [
    # Nuevos endpoints
    path('', views.ModelMoviesView.as_view(), name='movie_list'),
    path('<int:pk>', views.MovieDetailView.as_view(), name='movie_detail'),
    path('rate_movie/<int:movie_id>/<int:rating>/', views.rate_movie, name='rate_movie'),

    # Anteriores endpoints
    path('old', views.ModelOldMoviesView.as_view(), name='movie_list'),
    path('old/<int:pk>', views.MovieOldDetailView.as_view(), name='movie_detail'),
]
