from django.urls import path
from administracion.views import administracion
from registroTrabajador.views import registroTrabajador
from registroProveedor.views import registroProveedor
from RegEmpConv.views import registroEmpresa
from RegisterPlatillo.views import registroPlatillo
from listarPlatillos.views import listarPlatillos, eliminarPlatillo
from actualizarPlatillo.views import modificarPlatillo

url_patterns = [
    path('',administracion),
    path('trabajador',registroTrabajador),
    path('proveedor',registroProveedor),
    path('empresa',registroEmpresa),
    path('platillo',registroPlatillo),
    path('modificarPlatillo/<id>/', modificarPlatillo),
    path('eliminarPlatillo/<id>', eliminarPlatillo),
    path('listarPlatillos', listarPlatillos)
]
