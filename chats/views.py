from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Conversation, Message
from login.models import User

from django.shortcuts import render

# Create your views here.
@login_required(login_url='login') 
def chats(request):
    return render(request, 'chats/chats.html')

@login_required
def obtener_contactos(request):
    usuarios = User.objects.exclude(id=request.user.id)
    
    contactos = []
    for usuario in usuarios:
        conversacion = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=usuario
        ).first()
        
        contactos.append({
            'id': usuario.id,
            'username': usuario.username,
            'tiene_conversacion': bool(conversacion)
        })
    
    return render(request, 'chats/partials/lista_contactos.html', {
        'contactos': contactos
    })

@login_required
def obtener_mensajes(request, user_id):
    try:
        otro_usuario = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return render(request, 'chats/partials/error.html', {
            'error': 'Usuario no encontrado'
        })
    
    # Obtener o crear conversación usando el manager
    conversacion, created = Conversation.objects.get_or_create_for_users(
        request.user, 
        otro_usuario
    )
    
    # Obtener mensajes ordenados cronológicamente
    mensajes = Message.objects.filter(
        conversation=conversacion
    ).order_by('timestamp').select_related('sender')
    
    return render(request, 'chats/partials/lista_mensajes.html', {
        'mensajes': mensajes,
        'usuario_actual': request.user
    })