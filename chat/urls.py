"""
URL configuration for chat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import logout_then_login

from django.conf import settings 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Vista hacia la página principal
    path('chats/', include('chats.urls')),  # Vista hacia la página principal de chats
    path('login/', include('login.urls')),  # Vista hacia la página de inicio de sesión
    path('register/', include('register.urls')),  # Vista hacia la página de registro
    path('logout/', logout_then_login, name='logout'),  # Vista hacia la página de cierre de sesión
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)