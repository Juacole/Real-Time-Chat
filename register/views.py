from django.contrib import messages
from django.shortcuts import redirect, render
from login.models import User

# Create your views here.
def register(request):
    print("POST:", request.POST)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        if not first_name or not last_name or not username or not password or not email or not phone:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('/register/')
        
        user = User.objects.filter(username=username)
        
        if user.exists():
            messages.info(request, "El nombre de usuario ya esta en uso!")
            return redirect('/register/')
        
        User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
            phone=phone
        )

        messages.info(request, "Cuenta creada existosamente!")
        return redirect('/register/')
    
    return render(request, 'register/register.html')