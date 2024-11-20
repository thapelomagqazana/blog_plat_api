from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

def send_notification(user, message):
    """
    Sends a real-time notification to a specific user via WebSocket, if the channel layer is configured, 
    and creates a Notification record in the database.

    Args:
        user (CustomUser): The user to whom the notification will be sent.
        message (str): The notification message.

    Workflow:
        1. Creates a Notification instance for the user.
        2. Checks if the channel layer is configured.
        3. Sends a message to the WebSocket group associated with the user if the channel layer is available.

    WebSocket Message Format:
        - type: 'send_notification' (the method to invoke on the WebSocket consumer).
        - notification: A dictionary containing the notification details.
    """
    # Create a Notification instance in the database
    notification = Notification.objects.create(user=user, message=message)

    # Get the channel layer for WebSocket communication
    channel_layer = get_channel_layer()

    # Check if the channel layer is configured
    if channel_layer is not None:
        # Send the notification to the WebSocket group
        async_to_sync(channel_layer.group_send)(
            f'notifications_{user.id}',  # Group name based on user ID
            {
                'type': 'send_notification',  # WebSocket consumer method to invoke
                'notification': {
                    'id': notification.id,
                    'message': notification.message,
                    'is_read': notification.is_read,
                    'created_at': str(notification.created_at),  # Convert datetime to string
                }
            }
        )





