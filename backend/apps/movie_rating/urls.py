from django.urls import path
from . import views

# http://127.0.0.1:8000/movie_rating/...
app_name='movie_rating'
urlpatterns = [
    path('rate_movie/<int:movie_id>', views.MovieRateView.as_view(), name='rate_movie'),
    path('user_rating/<int:user_id>', views.MovieUserRatingView.as_view(), name='user_rating'),
]
