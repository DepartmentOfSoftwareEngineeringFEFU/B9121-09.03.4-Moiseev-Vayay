import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from brokers.tinkoff_stream import main


# class ArbitrageConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         await self.send(text_data=json.dumps({
#             'message': 'Received!',
#             'data': data
#         }))
#tinkof
class TinkoffPriceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("🧩 WebSocket connected, starting Tinkoff stream...")

        async def send_to_client(price):
            await self.send(text_data=json.dumps({
                "price": price
            }))

        self.stream_task = asyncio.create_task(
            main("BBG004730N88", send_to_client)
        )

    async def disconnect(self, code):
        if hasattr(self, 'stream_task'):
            self.stream_task.cancel()