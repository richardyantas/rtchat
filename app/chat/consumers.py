from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from .models import *
import json
from app.logger import logger
from django.contrib.auth import get_user_model


User = get_user_model()

class ChatroomConsumer(WebsocketConsumer):

    def connect(self):
        logger.info("connected")
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            # Si el usuario no está autenticado, rechaza la conexión
            self.close()
            return
        # Asegúrate de que self.user sea una instancia de User
        if not isinstance(self.user, User):
            self.user = User.objects.get(id=self.user.id)
        self.chatroom_name = self.scope["url_route"]["kwargs"]["chatroom_name"]
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, self.channel_name
        )
        if self.user not in self.chatroom.users_online.all():
            self.chatroom.users_online.add(self.user)
            self.update_online_count()

        self.accept()

    def disconnect(self, close_code):
        logger.info("disconnected")
        if hasattr(self, 'chatroom_name') and hasattr(self, 'user') and hasattr(self, 'chatroom'):
            async_to_sync(self.channel_layer.group_discard)(
                self.chatroom_name, self.channel_name
            )

            if self.user in self.chatroom.users_online.all():
                self.chatroom.users_online.remove(self.user)
                self.update_online_count()

    def receive(self, text_data):
        logger.info("received data")
        text_data_json = json.loads(text_data)
        body = text_data_json["body"]

        message = GroupMessage.objects.create(
            body=body, author=self.user, group=self.chatroom
        )

        event = {"type": "message_handler", "message_id": message.id}

        async_to_sync(self.channel_layer.group_send)(self.chatroom_name, event)

    def message_handler(self, event):
        message_id = event["message_id"]
        message = GroupMessage.objects.get(id=message_id)
        context = {
            "message": message,
            "user": self.user,
        }
        html = render_to_string("chat/partials/chat_message_p.html", context=context)
        self.send(text_data=html)

    def update_online_count(self):
        online_count = self.chatroom.users_online.count() - 1
        event = {"type": "online_count_handler", "online_count": online_count}
        async_to_sync(self.channel_layer.group_send)(self.chatroom_name, event)

    def online_count_handler(self, event):
        online_count = event["online_count"]
        html = render_to_string(
            "chat/partials/online_count.html", {"online_count": online_count}
        )
        self.send(text_data=html)
