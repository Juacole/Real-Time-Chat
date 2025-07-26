# Chat en Tiempo Real con Django Channels

## Descripción

Este proyecto es una aplicación de chat en tiempo real desarrollada con Django y Django Channels. Permite a los usuarios registrarse, iniciar sesión y mantener conversaciones privadas en tiempo real utilizando WebSockets.

## Características

- **Autenticación de usuarios**: Sistema completo de registro e inicio de sesión con modelo de usuario personalizado.
- **Chat en tiempo real**: Comunicación instantánea entre usuarios mediante WebSockets.
- **Conversaciones privadas**: Chats uno a uno entre usuarios registrados.
- **Interfaz responsiva**: Diseño adaptable a diferentes dispositivos.
- **Persistencia de mensajes**: Todos los mensajes se almacenan en la base de datos.
- **Indicador de lectura**: Sistema para marcar mensajes como leídos.

## Tecnologías utilizadas

- **Django 4.2.13**: Framework web de Python.
- **Django Channels 4.0.0**: Extensión de Django para manejar WebSockets y comunicación asíncrona.
- **Daphne 4.1.0**: Servidor ASGI para Django.
- **Redis 5.0.1**: Almacenamiento en memoria para gestionar canales de comunicación.
- **MySQL**: Base de datos relacional para almacenamiento persistente.
- **Docker**: Contenedores para facilitar el despliegue y desarrollo.

## Estructura del proyecto

```
├── chat/                  # Configuración principal del proyecto Django
├── chats/                 # Aplicación para la funcionalidad de chat
├── core/                  # Aplicación principal del proyecto
├── login/                 # Aplicación para la autenticación de usuarios
├── register/              # Aplicación para el registro de usuarios
├── docker-compose.yaml    # Configuración de Docker para desarrollo
└── requirements.txt       # Dependencias del proyecto
```

## Instalación y configuración

### Requisitos previos

- Python 3.8 o superior
- Docker y Docker Compose (opcional, para entorno de desarrollo)
- MySQL
- Redis

### Instalación manual

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/Real-Time-Chat.git
   cd Real-Time-Chat
   ```

2. Crear un entorno virtual e instalar dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configurar la base de datos en `chat/settings.py`.

4. Ejecutar migraciones:
   ```bash
   python manage.py migrate
   ```

5. Iniciar el servidor:
   ```bash
   python manage.py runserver
   ```

### Instalación con Docker

1. Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:
   ```
   MYSQL_DATABASE=chat_app
   MYSQL_ROOT_PASSWORD=tu_contraseña_root
   MYSQL_USER=tu_usuario
   MYSQL_PASSWORD=tu_contraseña
   ```

2. Iniciar los contenedores:
   ```bash
   docker-compose up -d
   ```

3. Ejecutar migraciones:
   ```bash
   python manage.py migrate
   ```

4. Iniciar el servidor Django:
   ```bash
   python manage.py runserver
   ```

## Uso

1. Acceder a la aplicación en `http://localhost:8000`
2. Registrarse como nuevo usuario o iniciar sesión
3. Iniciar una conversación con otro usuario registrado
4. ¡Comenzar a chatear en tiempo real!

## Arquitectura

### WebSockets

La aplicación utiliza WebSockets a través de Django Channels para proporcionar comunicación en tiempo real. Cada conversación privada tiene su propio grupo de canales, lo que permite que los mensajes se envíen instantáneamente entre los participantes.

### Modelo de datos

- **User**: Modelo personalizado que extiende AbstractUser de Django, añadiendo campos adicionales como número de teléfono.
- **Conversation**: Representa una conversación entre dos usuarios.
- **Message**: Almacena los mensajes individuales dentro de una conversación.

## Contribución

1. Hacer un fork del repositorio
2. Crear una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Hacer commit de tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Hacer push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## Contacto

Para preguntas o sugerencias, por favor contacta a [tu-email@ejemplo.com](mailto:tu-email@ejemplo.com).