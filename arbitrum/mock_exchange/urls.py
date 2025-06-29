from django.urls import path
from .views import *

urlpatterns = [
    path('api/stream/<str:ticker>/', RealtimePriceView.as_view(), name='stream-price'),
]
