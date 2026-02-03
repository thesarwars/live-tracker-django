import json
from channels.generic.websocket import AsyncWebsocketConsumer

from asgiref.sync import sync_to_async

from django.contrib.auth.models import AnonymousUser

from accountsio.choices import UserTypeChoices
# from .mode


class TrackerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("data in scope", self.scope)
        self.user = self.scope.get("user", AnonymousUser())
        self.receiver_id = self.scope["url_route"]["kwargs"]["receiver_id"]
        self.order_id = self.scope["url_route"]["kwargs"]["order_id"]
        
        if self.user.is_anonymous:
            await self.close()
            return
        
        if self.user.user_type != UserTypeChoices.RIDER:
            await self.close()
            return
        
        key = f"order:{self.order_id}:location"
        self.group_name = key
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        
    async def receive(self, text_data):
        data = json.loads(text_data)
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        
        # receiver = await sync_to_async(User.objects.get)(id=self.receiver_id)
        
        
        if latitude is not None and longitude is not None:
            location_data = {
                "receiver_id": self.receiver_id,
                "order_id": self.order_id,
                "latitude": latitude,
                "longitude": longitude,
            }
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "send_location",
                    "location_data": location_data,
                },
            )
        
    async def send_location(self, event):
        location_data = event["location_data"]
        await self.send(text_data=json.dumps(location_data))


class CustomerTrackerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("customer scope", self.scope)
        self.user = self.scope.get("user", AnonymousUser())
        self.order_id = self.scope["url_route"]["kwargs"]["order_id"]

        if self.user.is_anonymous:
            await self.close()
            return

        if self.user.user_type != UserTypeChoices.CUSTOMER:
            await self.close()
            return

        key = f"order:{self.order_id}:location"
        self.group_name = key
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Customers don't send location; ignore or validate as needed
        return

    async def send_location(self, event):
        location_data = event["location_data"]
        await self.send(text_data=json.dumps(location_data))