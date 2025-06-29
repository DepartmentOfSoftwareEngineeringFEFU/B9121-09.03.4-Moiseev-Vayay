from django.core.management.base import BaseCommand
from tinkoff.invest import AsyncClient
from brokers.models import AssetTinkoff
import asyncio
import os

from asgiref.sync import sync_to_async
TOKEN = 't.mm4Yd8ystZ4erLgjgi4qXqYZA-Bq2XKhdNB7qsZ5p-3O6j4xcpzs1S3EJ7gub_FADrO4Le9dyPzihETCXfWGvg'

@sync_to_async
def save_asset(figi, ticker, class_code, name):
    asset, created = AssetTinkoff.objects.update_or_create(
        figi=figi,
        defaults={
            "ticker": ticker,
            "class_code": class_code,
            "name": name,
        }
    )
    return asset, created


class Command(BaseCommand):
    help = "Загрузка акций из Тинькофф API"

    def handle(self, *args, **kwargs):
        asyncio.run(self.load_assets())

    async def load_assets(self):
        async with AsyncClient(TOKEN) as client:
            shares = await client.instruments.shares()

            for instrument in shares.instruments:
                asset, created = await save_asset(
                    instrument.figi,
                    instrument.ticker,
                    instrument.class_code,
                    instrument.name,
                )
                action = "✅ Добавлен" if created else "🔄 Обновлён"
                self.stdout.write(f"{action}: {asset.ticker} — {asset.name}")