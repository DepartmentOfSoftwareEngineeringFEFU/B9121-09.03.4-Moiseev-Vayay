from django.urls import path
from .views import RegisterView, LoginView, ProfileView, tariff_list_api, profile_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', profile_view, name='profile'),
    path('api/tariffs/', tariff_list_api, name='tariff-list'),
]