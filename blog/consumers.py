import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer to handle real-time notifications for authenticated users.

    Methods:
        connect(): Handles a new WebSocket connection. Authenticated users are added to a notification group.
        disconnect(close_code): Handles WebSocket disconnection. Removes the user from the notification group.
        receive(text_data): Handles incoming messages from the WebSocket. (Not implemented here.)
        send_notification(event): Sends a notification message to the WebSocket client.
    """

    async def connect(self):
        """
        Handles a new WebSocket connection.

        - Checks if the user is authenticated.
        - Adds the user to a group named `notifications_<user_id>`.
        - Accepts the WebSocket connection if the user is authenticated, otherwise closes it.
        """
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(
                f'notifications_{self.user.id}',
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        """
        Handles WebSocket disconnection.

        - Removes the user from the `notifications_<user_id>` group.

        Args:
            close_code (int): The WebSocket close code.
        """
        await self.channel_layer.group_discard(
            f'notifications_{self.user.id}',
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Handles incoming messages from the WebSocket client. (Currently not implemented.)

        Args:
            text_data (str): The received text data.
        """
        pass

    async def send_notification(self, event):
        """
        Sends a notification message to the WebSocket client.

        Args:
            event (dict): The event data containing the notification.
        """
        await self.send(text_data=json.dumps(event['notification']))
