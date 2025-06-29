#C:\Users\Дмитрий\Desktop\документы\вкр\arbitrum
from django.urls import path
#from arbitrage.consumer import ArbitrageConsumer
from arbitrage.consumer import TinkoffPriceConsumer

websocket_urlpatterns = [
  #  path('ws/arbitrage/', ArbitrageConsumer.as_asgi()),
    path('ws/stream/', TinkoffPriceConsumer.as_asgi()),
]