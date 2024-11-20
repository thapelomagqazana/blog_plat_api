from django.urls import path
from .consumers import NotificationConsumer

# WebSocket URL patterns for handling real-time notifications
websocket_urlpatterns = [
    path('ws/notifications/', NotificationConsumer.as_asgi()),
]