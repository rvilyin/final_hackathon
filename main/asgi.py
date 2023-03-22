"""
ASGI config for main project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""



# mysite/asgi.py
import os
import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from applications.chat.middleware import JwtAuthMiddlewareStack


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
django.setup()

import applications.chat.routing

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": JwtAuthMiddlewareStack(
        URLRouter(
            applications.chat.routing.websocket_urlpatterns
        )
    ),
})