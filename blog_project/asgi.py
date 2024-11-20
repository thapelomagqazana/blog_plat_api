"""
ASGI config for blog_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from blog.routing import websocket_urlpatterns

# Set the default settings module for the Django application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')

"""
Main ASGI application entry point.

Routes incoming connections based on their protocol type.

Protocols:
    "http": Handles standard HTTP connections using Django's ASGI application.
    "websocket": Handles WebSocket connections with authentication support.
"""
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        # Middleware stack that provides authentication for WebSocket connections.
        # Wraps the WebSocket routing layer with session-based authentication.
        URLRouter(
            # Defines the routing for WebSocket connections using `websocket_urlpatterns`.
            # `websocket_urlpatterns`: A list of URL patterns for WebSocket routes defined in `blog.routing`.
            websocket_urlpatterns
        )
    ),
})
