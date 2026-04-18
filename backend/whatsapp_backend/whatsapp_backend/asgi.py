import os
import django

# from channels.auth import AuthMiddlewareStack   # ✅ ADD THIS



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whatsapp_backend.settings')
django.setup()   # ✅ ADD THIS

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from websocket.routing import websocket_urlpatterns
from websocket.middleware import JWTAuthMiddleware


application = ProtocolTypeRouter({
    "http": get_asgi_application(),

     "websocket": JWTAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})