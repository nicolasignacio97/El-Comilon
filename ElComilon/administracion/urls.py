from django.urls import path
from administracion.views import administracion
from registroTrabajador.views import registroTrabajador
from registroProveedor.views import registroProveedor
from RegEmpConv.views import registroEmpresa
from RegisterPlatillo.views import registroPlatillo
from RegCliConv.views import RegistroCliConvenio, listarCliConv, modificarCliConv, eliminarCliConv

url_patterns = [
    path('',administracion),
    path('trabajador',registroTrabajador),
    path('proveedor',registroProveedor),
    path('empresa',registroEmpresa),
    path('platillo',registroPlatillo),
    path('ClienteConvenio',RegistroCliConvenio),
    path('listarCliConv',listarCliConv),
    path('modCliConv/<id>',modificarCliConv),
    path('eliminar/<id>',eliminarCliConv),
]
