from django.db import models
from django.utils import timezone
from login.models import User
from django.core.exceptions import ValidationError

class ConversationManager(models.Manager):
    def get_or_create_for_users(self, user1, user2):
        # Ordenar los IDs para garantizar consistencia
        ids = sorted([user1.id, user2.id])
        unique_id = f"chat_{ids[0]}_{ids[1]}"
        
        # Buscar o crear conversación
        conversation, created = self.get_or_create(
            unique_id=unique_id,
            defaults={'created_at': timezone.now()}
        )
        
        # Añadir participantes si es nueva
        if created:
            conversation.participants.add(user1, user2)
        
        return conversation, created

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    unique_id = models.CharField(max_length=50, unique=True, blank=True)  # Campo para unicidad
    
    objects = ConversationManager()

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Conversación'
        verbose_name_plural = 'Conversaciones'

    def __str__(self):
        usernames = [user.username for user in self.participants.all()]
        return f"Chat entre {', '.join(usernames)}"
    
    def clean(self):
        # Validar que haya exactamente 2 participantes
        if self.participants.count() != 2:
            raise ValidationError("Las conversaciones deben tener exactamente 2 participantes")

class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}..."