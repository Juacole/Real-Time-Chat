from django.urls import path
from . import views

urlpatterns = [
    path('', views.chats, name='chats'),
    path('obtener-contactos/', views.obtener_contactos, name='obtener_contactos'),
    path('obtener-mensajes/<int:user_id>/', views.obtener_mensajes, name='obtener_mensajes'),
]