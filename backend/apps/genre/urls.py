from django.urls import path

# http://127.0.0.1:8000/genre/...
app_name='genre'
urlpatterns = [
    path('', views.ModelView.as_view(), name='model_create'),
]
