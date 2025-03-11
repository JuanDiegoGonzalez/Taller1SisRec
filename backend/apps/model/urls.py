from django.urls import path
from . import views

# http://127.0.0.1:8000/model/...
app_name='model'
urlpatterns = [
    path('', views.ModelView.as_view(), name='model_create'),
    path("train-model", views.ModelTrainView.as_view(), name="train_model"),
    path('old', views.ModelOldCreateView.as_view(), name='model_create'),
    path('old/result', views.ModelOldResultView.as_view(), name='model_result'),
]
