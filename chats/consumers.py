import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from login.models import User
from .models import Conversation, Message

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        self.user = self.scope["user"]
        self.other_user_id = self.scope['url_route']['kwargs']['user_id']
        
        if not await self.user_exists(self.other_user_id):
            await self.close()
            return

        self.conversation = await self.get_or_create_conversation()
        self.room_group_name = f'private_chat_{self.conversation.id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        
        message = await self.save_message(message_content)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'sender_id': self.user.id,
                'sender_username': self.user.username,
                'timestamp': str(message.timestamp),
                'message_id': message.id
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_username': event['sender_username'],
            'timestamp': event['timestamp'],
            'message_id': event['message_id']
        }))

    @database_sync_to_async
    def user_exists(self, user_id):
        return User.objects.filter(id=user_id).exists()

    @database_sync_to_async
    def get_or_create_conversation(self):
        other_user = User.objects.get(id=self.other_user_id)
        return Conversation.objects.get_or_create_for_users(self.user, other_user)[0]

    @database_sync_to_async
    def save_message(self, content):
        return Message.objects.create(
            conversation=self.conversation,
            sender=self.user,
            content=content
        )