from django.urls import path
from . import views

# http://127.0.0.1:8000/model/...
app_name='model'
urlpatterns = [
    path('', views.ModelCreateView.as_view(), name='model_create'),
    path('result', views.ModelResultView.as_view(), name='model_result'),
]
