from django.urls import re_path
from . import consumers

'''Establece las conexiones que tendra cada usuario, como se redirigen y como se organizan las conexiones WebSocket.

- Define como y auqe consmidor se va a conectar cada usuario segun la URL
- Permite que cada conexion websocket llegue al consumidor adecuado, segun la ruta y los parametros, como por ejemplo el nombre de la sala de chat'''
websocket_urlpatterns = [
    re_path(
        r'ws/private-chat/(?P<user_id>\d+)/$', 
        consumers.PrivateChatConsumer.as_asgi()
    ),
]