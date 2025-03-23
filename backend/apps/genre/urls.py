from django.urls import path
from .views import ModelGenresView, ModelAllGenresView

# http://127.0.0.1:8000/genre/...
app_name='genre'
urlpatterns = [
    path('movies/<int:genre_id>', ModelGenresView.as_view(), name='movies_genre'),
    path('all', ModelAllGenresView.as_view(), name='all_genres'),
]
