from django.shortcuts import render
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Asset
from decimal import Decimal
from django.core.cache import cache

TICKER_CONFIG = {
    "SBER": {"start_price": 313.00, "fluctuation": (-1.5, 1.5)},
    "GAZP": {"start_price": 125.00, "fluctuation": (-3, 1.5)},
    "YAND": {"start_price": 4159.00, "fluctuation": (-1.5, 1.5)},
    "TATN": {"start_price": 648.00, "fluctuation": (-3, 3)},
}

# Create your views here.
class RealtimePriceView(APIView):
     def get(self, request, ticker):
        try:
            ticker = ticker.upper()
            asset = Asset.objects.get(ticker=ticker)

            config = TICKER_CONFIG.get(ticker)
            if not config:
                return Response({"error": "Нет конфигурации для этого тикера"}, status=400)

            counter_key = f"price_counter_{ticker}"
            price_key = f"current_price_{ticker}"

            request_count = cache.get(counter_key, 0) + 1
            cache.set(counter_key, request_count, timeout=None)

            current_price = cache.get(price_key, config["start_price"])

            if request_count % 5 == 0:
                min_f, max_f = config["fluctuation"]
                fluctuation = random.uniform(min_f, max_f)
                new_price = round(float(current_price) + fluctuation, 2)
                current_price = new_price
                cache.set(price_key, current_price, timeout=None)
                asset.last_price = Decimal(new_price)
                asset.save(update_fields=[])

            return Response({
                "ticker": ticker,
                "price": float(current_price),
                "request_count": request_count
            })

        except Asset.DoesNotExist:
            return Response({"error": "Актив не найден"}, status=404)