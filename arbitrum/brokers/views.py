import asyncio
from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from tinkoff.invest import AsyncClient
from tinkoff.invest.utils import quotation_to_decimal

from tinkoff.invest import CandleInterval
from datetime import datetime, timedelta
import pytz

from brokers.models import AssetTinkoff

# finam
from finam_trade_api.client import Client
from finam_trade_api.candles.model import DayCandlesRequestModel, DayInterval
from finam_trade_api.candles.model import IntraDayCandlesRequestModel, IntraDayInterval

TOKEN = 't.mm4Yd8ystZ4erLgjgi4qXqYZA-Bq2XKhdNB7qsZ5p-3O6j4xcpzs1S3EJ7gub_FADrO4Le9dyPzihETCXfWGvg'
# finam token
FINAM_TOKEN = 'CAEQ+ov+BxoYYXfLq7xusew7wLoTY4S0zWzpEUbdrqUE'
FINAM_CLIENT_ID = '928879RIIT3'
client = Client(FINAM_TOKEN)

def get_tinkoff_assets(request):
    assets = AssetTinkoff.objects.all().values("ticker", "figi", "name")
    return JsonResponse({"assets": list(assets)})

def get_price(request):
    print("✅ get_price был вызван!")
    figi = request.GET.get("figi", "BBG004730RP0")

    async def get_data():
        try:
            async with AsyncClient(TOKEN) as client:
                response = await client.market_data.get_last_prices(figi=[figi])
                if not response.last_prices:
                    raise ValueError(f"Не найдена цена по FIGI: {figi}")
                price = quotation_to_decimal(response.last_prices[0].price)
                return float(price)
        except Exception as e:
            print("❌ Ошибка внутри get_data:", e)
            raise  # пробросим дальше для внешнего обработчика

    try:
        price = asyncio.run(get_data())
        return JsonResponse({"figi": figi, "price": price})
    except Exception as e:
        print("❌ Ошибка при получении цены:", e)
        return JsonResponse({"error": f"Ошибка получения цены: {str(e)}"}, status=500)
    
    

async def get_history(request):
    figi = request.GET.get("figi", "BBG004730RP0")
    days = int(request.GET.get("days", 1))

    now_utc = datetime.now(tz=pytz.UTC)
    from_utc = now_utc - timedelta(days=days)
    try:
        async with AsyncClient(TOKEN) as client:
            response = await client.market_data.get_candles(
                figi=figi,
                from_=from_utc,
                to=now_utc,
                interval=CandleInterval.CANDLE_INTERVAL_15_MIN
            )

            candles = [{
                "time": candle.time.isoformat(),
                "price": float(quotation_to_decimal(candle.close))
            } for candle in response.candles]
            #print("📈 Загружено свечей:", len(candles))
            return JsonResponse({"figi": figi, "candles": candles})
    except Exception as e:
        print("❌ Ошибка при загрузке истории:", e)
        return JsonResponse({"error": str(e)}, status=500)
    #===================finam ==============
    
def get_finam_history(request):
    code = request.GET.get("code", "SBER").strip().replace('"', '').upper()

    now = datetime.now()
    from_date = now - timedelta(hours=24)

    async def get_data():
        params = IntraDayCandlesRequestModel(
            securityBoard="TQBR",
            securityCode=code,
            timeFrame=IntraDayInterval.M15,
            intervalFrom=from_date.strftime("%Y-%m-%d %H:%M:%S"),
            intervalTo=now.strftime("%Y-%m-%d %H:%M:%S"),
            count=96  # 96 * 15 мин = 24 часа
        )
        return await client.candles.get_in_day_candles(params)

    try:
        candles = asyncio.run(get_data())
        return JsonResponse({
            "code": code,
            "candles": [
                {
                    "time": c.timestamp,  # Важно!
                    "price": c.close.num / (10 ** c.close.scale)
                }
                for c in candles
            ]
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def get_finam_price(request):
    code = request.GET.get("code", "SBER").strip().replace('"', '').upper()

    async def get_data():
        now = datetime.now()
        from_date = now - timedelta(hours=24)

        params = IntraDayCandlesRequestModel(
            securityBoard="TQBR",
            securityCode=code,
            timeFrame=IntraDayInterval.M15,
            intervalFrom=from_date.strftime("%Y-%m-%d %H:%M:%S"),
            intervalTo=now.strftime("%Y-%m-%d %H:%M:%S"),
            count=96
        )
        return await client.candles.get_in_day_candles(params)

    try:
        candles = asyncio.run(get_data())

        if not candles:
            return JsonResponse({"error": "Нет данных от Finam"}, status=404)

        last = candles[-1]
        price = last.close.num / (10 ** last.close.scale)

        return JsonResponse({"price": price})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)