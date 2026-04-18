import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack   # ✅ ADD THIS
from django.core.asgi import get_asgi_application
from websocket.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whatsapp_backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),

    "websocket": AuthMiddlewareStack(   # ✅ IMPORTANT
        URLRouter(
            websocket_urlpatterns
        )
    ),
})