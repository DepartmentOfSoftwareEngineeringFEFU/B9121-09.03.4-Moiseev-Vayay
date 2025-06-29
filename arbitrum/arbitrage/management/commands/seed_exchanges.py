from django.core.management.base import BaseCommand
from brokers.models import Exchange, Tariff

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        exchanges = [
            {
                "name": "Tinkoff",
                "code": "TINK",
                "api_url": "https://api-invest.tinkoff.ru/openapi",
                "tariffs": [
                    {"name": "Инвестор", "commission": 0.10},
                    {"name": "Трейдер", "commission": 0.05},
                    {"name": "Премиум", "commission": 0.04},
                ]
            },
            {
                "name": "Finam",
                "code": "FINAM",
                "api_url": "https://api.finam.ru",
                "tariffs": [
                    {"name": "Долгосрочный портфель", "commission": 0.28},
                    {"name": "Стратег", "commission": 0.05},
                    {"name": "Инвестор", "commission": 0.35},
                    {"name": "Единый консультационный", "commission": 0.10},
                ]
            },
        ]   
        for ex_data in exchanges:
            exchange, created = Exchange.objects.get_or_create(
                code=ex_data["code"],
                defaults={
                    "name": ex_data["name"],
                    "api_url": ex_data["api_url"]
                }
            )
            if created:
                    self.stdout.write(f"✅ Добавлена биржа: {exchange.name}")
            elif not created:
                updated = False
                if not exchange.api_url and ex_data["api_url"]:
                    exchange.api_url = ex_data["api_url"]
                    updated = True
                if not exchange.name and ex_data["name"]:
                    exchange.name = ex_data["name"]
                    updated = True
                if updated:
                    exchange.save()
                    self.stdout.write(f"🔄 Обновлена информация о бирже: {exchange.name}")

                # Добавление тарифов
            for tariff_data in ex_data["tariffs"]:
                    tariff, created_tariff = Tariff.objects.get_or_create(
                        exchange=exchange,
                        name=tariff_data["name"],
                        defaults={"commission": tariff_data["commission"]}
                    )
                    if created_tariff:
                        self.stdout.write(f"  ➕ Тариф добавлен: {tariff.name} ({tariff.commission}%)")
                    else:
                        self.stdout.write(f"  ⏩ Тариф уже существует: {tariff.name}")

        self.stdout.write(self.style.SUCCESS("🎉 Загрузка бирж и тарифов завершена."))  