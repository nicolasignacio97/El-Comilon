"""ElComilon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from Home.views import inicio
from Login.views import login
from RegisterPlatillo.views import registroPlatillo
from Register.views import register
from registroProveedor.views import registroProveedor   
from reclamo.views import reclamo
from Home.views import quienesSomos
from administracion.urls import url_patterns
from PerfilUsuario.views import Usertemplate
from RegisterRepartidor.views import registroRep,RegisterRepatidor
from Pedido.views import pedido
from Platillos.views import platillos
from detallePedido.views import detallePedido

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',inicio),
    path('login/',include('Login.urls')),
    path('registroPlatillo',registroPlatillo),
    path('registro',register),  
    path('registroProveedor',registroProveedor),
    path('reclamo',reclamo),
    path('quienesSomos', quienesSomos),
    path('perfil', Usertemplate),
    path('registerrepartidor', RegisterRepatidor),
    path('regin', registroRep),
    path('pedido', pedido),
    path('platillos', platillos),
    path('detallePedido', detallePedido),
    path('administracion/', include(url_patterns))

]
