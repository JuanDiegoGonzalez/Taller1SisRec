from django.urls import path
from .views import home_view, login_view, logout_view, register, RegisterView

urlpatterns = [
    path('', home_view, name= 'home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path("accounts/register/", RegisterView.as_view(), name="register"),
]
