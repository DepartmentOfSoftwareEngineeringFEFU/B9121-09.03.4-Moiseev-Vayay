from django.urls import path
from .views import *

urlpatterns = [
    path("price/", get_price, name="get_price"),
    path("history/", get_history, name="get_history"),
    path("finam/history/", get_finam_history),
    path("finam/price/", get_finam_price),
    path("tinkoff/assets/", get_tinkoff_assets),
]