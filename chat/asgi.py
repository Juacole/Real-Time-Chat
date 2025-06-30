import os
import django


'''asgi.py es un piunto de entrada para servidores asincronos de Django, que permite manejar conexiones WebSocket y otros protocolos asíncronos.
- Configura el entorno Django para que pueda ser utilizado por ASGI.'''

# Configuracion del entorno Django
# Establece la variable de entorno DJANGO_SETTINGS_MODULE para que Django sepa dónde encontrar la configuración del proyecto.
# En este caso, se asume que el archivo de configuración se llama 'settings.py'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from chats.routing import websocket_urlpatterns


'''
- ProtocolTypeRouter: Permite enrutar diferentes tipos de conexiones (por ejemplo, HTTP o WebSocket).
- AuthMiddlewareStack: Añade soporte de autenticación para conexiones WebSocket.
- URLRouter: Usa las rutas definidas en websocket_urlpatterns para dirigir las conexiones WebSocket al consumidor adecuado.
'''
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(), # <-- Esto enruta las solicitudes HTTP normales
        "websocket": AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        ),
    }
)