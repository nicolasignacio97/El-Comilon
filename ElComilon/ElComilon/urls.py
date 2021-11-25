
from os import name
from django.contrib import admin
from django.urls import path, include
from recepcionista.views import viewRecepcionista,asignarRepartidor, cambiarEstado,menuRecepcion
from registroDeUsuarios.views import registroUsuario
from Home.views import inicio
from RegisterPlatillo.views import registroPlatillo
from proveedorMenu.views import menuProveedor
from repartidor.views import viewPedido, viewRepartidor,PerfilRepartidor,MiVehiculo
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
    path('', inicio, name="home"),
    path('admin/', admin.site.urls),
    path('administracion/', include(url_patterns)),
    path('registroPlatillo', registroPlatillo),
    path('reclamo', reclamo),
    path('quienesSomos', quienesSomos ,name= 'quienesSomos'),
    path('Historial/<id>', PerfilUsuario, name="historial"),  # despues id en la ruta para filtro
    path('pedido', pedido),
    path('platillos', platillos, name="platillos"),
    path('perfilMenu/<id>', perfilMenu, name="perfilMenu"),
    path('menuProveedor/<id>', menuProveedor, name="menuProveedor"),

    path('viewPedido/<id>', viewPedido),
    path('repartidor', viewRepartidor, name="repartidor"),
    path('perfilRepartidor/<id>', PerfilRepartidor, name="perfilRepartidor"),
    path('detallePedido', detallePedido),
    path('detallePedido/<idpedido>/<id>', detallePedido),
    path('MiVehiculo/<id>', MiVehiculo, name='MiVehiculo'),
    
    path('registroUsuarios', registroUsuario,name='registro'),
    path('cambioContrasena', CambiarContra, name="cambioContrasena"),
 

    path('menu/<id>', menu, name="menu"),
    path('crearMenu/<id>', crearMenu, name="crearMenu"),
    
    path('accounts/', include('django.contrib.auth.urls')),
    path('viewPedido/<id>', viewPedido),
         
    path('recepcionista', viewRecepcionista, name='recepcionista'),
    path('estado/<id>', cambiarEstado, name='estado'),
    path('asignacion/<id>', asignarRepartidor, name='asignacionRepartidor'),
    path('menuRecepcion/<id>', menuRecepcion, name='menuRecepcion'),
    # carro
    path('agregar/<id>', agregar_producto, name="agregarProducto"),
    path('eliminar/<id>', eliminar_producto, name="eliminar"),
    path('restar/<id>', restar_producto, name="restar_producto"),
    path('limpiarCarro', limpiar_carrito, name="limpiar_carrito"),
    path('guardar', guardar, name="guardar"),
    path('prueba/', pag_404)
]
# handler404 = 'administracion.views.pag_404'

