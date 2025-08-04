import json
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


import logging
logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "sala_general"
        self.room_group_name = f"chat_{self.room_name}"
        query_string = self.scope['query_string'].decode()
        params = parse_qs(query_string)
        self.from_url = params.get('from_url', [''])[0]
        self.current_user = params.get('current_user', [''])[0]

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Notificar a los demás que se conectó alguien (excepto a sí mismo)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_event",
                "event": "connected",
                "channel": self.channel_name,
            }
        )

    async def disconnect(self, close_code):
        # Notificar a los demás que se desconectó alguien
        from cargosystem.views.desbloquear import desbloquear_modulo_usuario
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_event",
                "event": "disconnected",
                "channel": self.channel_name,
            }
        )
        await sync_to_async(desbloquear_modulo_usuario)(self.from_url, self.current_user)

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        if "message" in data:
            message = data["message"]

            # Transmitir el mensaje al grupo
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                }
            )

    async def chat_message(self, event):
        # Emitir mensaje normal al WebSocket
        await self.send(text_data=json.dumps({
            "type": "message",
            "message": event["message"],
        }))

    async def user_event(self, event):
        # Evitá que el socket que se desconecta reciba su propio evento
        if event["channel"] != self.channel_name:
            await self.send(text_data=json.dumps({
                "type": "event",
                "event": event["event"],
            }))
