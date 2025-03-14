from django.urls import path
from . import views

# http://127.0.0.1:8000/movie_rating/...
app_name='movie_rating'
urlpatterns = [
    # Nuevos endpoints
    path('', views.ModelMoviesView.as_view(), name='movie_list'),
    path('<int:pk>', views.MovieDetailView.as_view(), name='movie_detail'),
    path('rate_movie/<int:movie_id>', views.MovieRateView.as_view(), name='rate_movie'),
    path('user_rating', views.MovieUserRatingView.as_view(), name='user_rating'),

    # Anteriores endpoints
    path('old', views.ModelOldMoviesView.as_view(), name='movie_list'),
    path('old/<int:pk>', views.MovieOldDetailView.as_view(), name='movie_detail'),
]
