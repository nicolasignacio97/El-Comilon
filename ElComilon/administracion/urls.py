from django.urls import path
from administracion.views import administracion
from registroTrabajador.views import registroTrabajador
from registroProveedor.views import registroProveedor
from RegEmpConv.views import registroEmpresa
from RegisterPlatillo.views import registroPlatillo
from gestionRestaurantes.views import listarRestaurantes, modificarProveedor,EliminarProveedor,EliminarRepresentante,ModificarRepresentante

url_admin = [
    path('',administracion),
    path('trabajador',registroTrabajador),
    path('proveedor',registroProveedor),
    path('empresa',registroEmpresa),
    path('platillo',registroPlatillo),
    path('listarProveedores',listarRestaurantes),
    path('modificarProveedor/<id>/',modificarProveedor),
    path('eliminarProveedor/<id>/',EliminarProveedor),
    path('eliminarRepresentante/<id>/',EliminarRepresentante),
    path('modificarRepresentante/<id>/',ModificarRepresentante),
]
