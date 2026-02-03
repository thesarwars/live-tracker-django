"""
ASGI config for master project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "master.settings")

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

application = get_asgi_application()

# from channels.auth import AuthMiddlewareStack

from trackerio.middleware import JWTAuthMiddleware
from trackerio.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": application,
        "websocket": JWTAuthMiddleware(URLRouter(websocket_urlpatterns)),
    }
)
