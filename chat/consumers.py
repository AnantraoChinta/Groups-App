import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Room, Message
from channels.db import database_sync_to_async

# Keep in sync with Message.message max_length
MAX_MESSAGE_LENGTH = 500


class ChatConsumer(AsyncWebsocketConsumer):

    # Looks up the room and confirms the connecting user is a participant.
    # This mirrors the check in chat.views.room -- the HTTP view alone is not
    # enough, since the socket can be opened directly without loading the page.
    @database_sync_to_async
    def _get_room_for_user(self, user):
        room = Room.objects.filter(name=self.room_name).first()
        if room is None:
            return None
        if not room.participants.filter(pk=user.pk).exists():
            return None
        return room

    @database_sync_to_async
    def _save_message(self, user, message):
        Message.objects.create(message=message, user=user, room=self.room)

    # Creates a channel connection
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["slug"]
        self.room_group_name = 'chat_%s' % self.room_name
        self.room = None

        user = self.scope.get("user")

        # Anonymous visitors get no socket at all
        if user is None or not user.is_authenticated:
            await self.close(code=4401)
            return

        # Nor do logged-in users who were never added to this room
        self.room = await self._get_room_for_user(user)
        if self.room is None:
            await self.close(code=4403)
            return

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    # Disconnects from room
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )



    # When a user sends a message, it will be sent from the JS function
    # through the WebSocket to the proper room
    
    # When a message is received, it is sent to function chat_message
    
    async def receive(self, text_data):
        # A rejected connection should never reach this, but do not trust it
        if self.room is None:
            await self.close(code=4403)
            return

        try:
            text_data_json = json.loads(text_data)
        except (ValueError, TypeError):
            return

        if not isinstance(text_data_json, dict):
            return

        message = text_data_json.get("message")
        if not isinstance(message, str):
            return

        # Drop blank messages, and cap the length so a client cannot push
        # arbitrarily large payloads past the model's max_length
        message = message.strip()[:MAX_MESSAGE_LENGTH]
        if not message:
            return

        user = self.scope["user"]

        await self._save_message(user, message)

        # Invoke the chat_message function below
        # Pass in the message
        await self.channel_layer.group_send(
            self.room_group_name, {"type" : "chat_message", "message" : message,
            "user" : user.username}
        )

    # Sends message
    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        
        
        await self.send(text_data = json.dumps({"message" : message, "user" : user}))
