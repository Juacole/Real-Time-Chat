import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        '''Cliente se conecta al WebSocket'''
        
        # Recogemos el nombre de la sala
        # Obtiene el nombre de la sala desde la URL
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"] 
        
        # Creamos el nombre del grupo de la sala
        self.room_group_name = "chat_%s" % self.room_name
        
        # Se une a la sala
        # Se agrega el canal del cliente al grupo de la sala, permitiendo que reciba mensajes enviados a ese grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # Se informa al cliente que se ha conectado
        await self.accept()
        
    # Si el cliente se desconecta, se ejecuta este método eliminando el canal del grupo de la sala    
    async def disconnect(self, close_code):
        '''Cliente se desconecta del WebSocket'''
        
        # Se sale de la sala
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    async def receive(self, text_data):
        '''Cliente enviar informacion y nosotros la recibimos'''
        
        text_data_json = json.loads(text_data) # Convierte el texto recibido en formato JSON a un diccionario
        
        # Extraemos el nombre y el texto del mensaje
        name = text_data_json["name"]
        text = text_data_json["text"]
        
        # Envía el mensaje a todos los miembros del grupo de la sala, llamando al método chat_message en cada consumidor del grupo.
        # Esto permite que todos los clientes conectados a la sala reciban el mensaje.
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "name": name,
                "text": text
            },
        )
    
    # Este método es llamado automáticamente cuando se recibe un mensaje del grupo y se encarga de enviar el mensaje al WebSocket del cliente.
    async def chat_message(self, event):
        '''Recibimos informacion de la sala'''
        
        name = event["name"]
        text = event["text"]
        
        # Se envia mensaje al WebSocket
        await self.send(text_data=json.dumps({
            "type": "chat_message",
            "name": name,
            "text": text
        }))