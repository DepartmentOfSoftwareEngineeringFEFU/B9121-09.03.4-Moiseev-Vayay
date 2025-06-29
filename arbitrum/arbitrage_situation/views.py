from django.http import JsonResponse
from django.shortcuts import render
import requests
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from arbitrage_situation.models import ArbitrageOpportunity
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

from rest_framework import status
LINK_TEMPLATES = {
    "TINK": "https://www.tbank.ru/invest/stocks/{code}/",
    "FINAM": "https://www.finam.ru/quote/moex/{code}/",
    "ALFA": "https://alfabank.ru/make-money/investments/catalog/akcii/t/{code}/"
}
TELEGRAM_BOT_TOKEN = "7818424408:AAECY9VFLT4wJMPIv_7_3vPb5Fcpm1uQ_0s"
TELEGRAM_CHAT_ID = "1985313887"
class ReportOpportunityView(APIView):
    def post(self, request):
        data = request.data

        required = ["asset", "exchange_from", "exchange_to", "price_from", "price_to", "profit", "profit_percent"]
        if not all(k in data for k in required):
            return Response({"error": "Missing fields"}, status=400)
        code = data.get("asset", "SBER").upper()
        link_from = LINK_TEMPLATES.get(data["exchange_from"], "").replace("{code}", code)
        link_to = LINK_TEMPLATES.get(data["exchange_to"], "").replace("{code}", code)

        obj, created = ArbitrageOpportunity.objects.update_or_create(
            asset=data["asset"],
            exchange_from=data["exchange_from"],
            exchange_to=data["exchange_to"],
            is_active=True,
            defaults={
                "price_from": data["price_from"],
                "price_to": data["price_to"],
                "profit": data["profit"],
                "profit_percent": data["profit_percent"],
                "updated_at": now(),
                "link_from": link_from,
                "link_to": link_to
            }
        )
        # телега
        if created:
            send_telegram_notification(obj)
            
        return Response({
            "status": "saved",
            "created": created,
            "created_at": obj.created_at,
            "updated_at": obj.updated_at,
            "id": obj.id
        })

def arbitrage_opportunities_json(request):
    situations = ArbitrageOpportunity.objects.filter(is_active=True).order_by("-updated_at")
    data = []
    for s in situations:
        data.append({
            "asset": s.asset,
            "exchange_from": s.exchange_from,
            "exchange_to": s.exchange_to,
            "price_from": float(s.price_from),
            "price_to": float(s.price_to),
            "profit": float(s.profit),
            "profit_percent": float(s.profit_percent),
            "link_from": s.link_from,
            "link_to": s.link_to,
        })
    return JsonResponse(data, safe=False)


# телега
def send_telegram_notification(opportunity):
    profile_url = "http://127.0.0.1:8000/profile/"
    message = (
        f"📈 Новая арбитражная ситуация!\n\n"
        f"🔹 Актив: {opportunity.asset}\n"
        f"🔻 Покупка ({opportunity.exchange_from}): {opportunity.price_from} ₽\n"
        f"🔺 Продажа ({opportunity.exchange_to}): {opportunity.price_to} ₽\n"
        f"💰 Профит: {opportunity.profit} ₽ ({opportunity.profit_percent}%)\n\n"
        f"👉 [Открыть в системе]({profile_url})"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        print("❌ Ошибка отправки в Telegram:", e)
 