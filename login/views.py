from django.contrib import messages
from django.shortcuts import redirect, render
from .models import User
from django.contrib.auth import authenticate, login as auth_login

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/chats/')
        else:
            messages.error(request, 'Usuario o contraseña inválidos.')
            return redirect('/login/')
    return render(request, 'login/login.html')
    