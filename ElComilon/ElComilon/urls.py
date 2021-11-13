from django.conf.urls import handler404
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from recepcionista.views import viewRecepcionista,asignarRepartidor, cambiarEstado
from registroDeUsuarios.views import registroUsuario
# from ElComilon.listarPlatillos.views import modificarPlatillo
from Home.views import inicio
from RegisterPlatillo.views import registroPlatillo
from Register.views import register, perfil
from registroProveedor.views import registroProveedor
from django.conf.urls import handler404

from repartidor.views import viewPedido, viewRepartidor
from reclamo.views import reclamo
from Home.views import quienesSomos
from administracion.urls import url_patterns
from PerfilUsuario.views import PerfilUsuario,perfilMenu,CambiarContra
from Pedido.views import pedido
from Platillos.views import platillos, agregar_producto, eliminar_producto, restar_producto, limpiar_carrito,guardar
from detallePedido.views import detallePedido
from Menu.views import menu, crearMenu
from administracion.views import pag_404



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio, name="home"),
    path('registroPlatillo', registroPlatillo),
    path('registro', register),
    path('registroProveedor', registroProveedor),
    path('reclamo', reclamo),
    path('quienesSomos', quienesSomos),
    path('Historial/<id>', PerfilUsuario, name="historial"),  # despues id en la ruta para filtro
    path('pedido', pedido),
    path('platillos', platillos, name="platillos"),
    path('perfilMenu/<id>', perfilMenu, name="perfilMenu"),
    path('viewPedido/<id>', viewPedido),
    path('repartidor', viewRepartidor, name="repartidor"),
    path('detallePedido', detallePedido),
    path('detallePedido/<idpedido>/<id>', detallePedido),
    path('registroUsuarios', registroUsuario),
    path('administracion/', include(url_patterns)),
    path('cambioContrasena', CambiarContra, name="cambioContrasena"),

    path('menu/<id>', menu, name="menu"),
    path('crearMenu/<id>', crearMenu, name="crearMenu"),


    path('accounts/', include('django.contrib.auth.urls')),
    path('viewPedido/<id>', viewPedido),     
    path('recepcionista', viewRecepcionista, name='recepcionista'),
    path('estado/<id>', cambiarEstado, name='estado'),
    path('asignacion/<id>', asignarRepartidor, name='asignacionRepartidor'),
    # carro
    path('agregar/<id>', agregar_producto, name="agregarProducto"),
    path('eliminar/<id>', eliminar_producto, name="eliminar"),
    path('restar/<id>', restar_producto, name="restar_producto"),
    path('limpiarCarro', limpiar_carrito, name="limpiar_carrito"),
    path('guardar', guardar, name="guardar"),
    path('prueba/', pag_404)
]
# handler404 = 'administracion.views.pag_404'

