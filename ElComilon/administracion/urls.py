from django.urls import path
from administracion.views import administracion
from registroTrabajador.views import registroTrabajador
from registroProveedor.views import registroProveedor
from RegEmpConv.views import registroEmpresa
from RegisterPlatillo.views import registroPlatillo
from registroTrabajador.views import listaTrabajador
from registroTrabajador.views import trabajadorRut
from registroTrabajador.views import actualizarTrabajador
from registroTrabajador.views import eliminarTrabajador
from RegEmpConv.views import listaEmpresa
from RegEmpConv.views import empresaRut
from RegEmpConv.views import eliminarEmpresa
from RegisterRepartidor.views import registroVeh,registroRep,editRepartidor,deleterepartidor,listarRep
from registroTrabajador.views import actTrabajador

url_patterns = [
    path('',administracion),
    path('trabajador',registroTrabajador),
    path('proveedor',registroProveedor),
    path('empresa',registroEmpresa),
    path('platillo',registroPlatillo),
    path('listaTrabajador',listaTrabajador),
    path('trabajadorRut',trabajadorRut),
    path('actualizarTrabajador', actualizarTrabajador),
    path('eliminarTrabajador',eliminarTrabajador),
    path('listaEmpresa', listaEmpresa),
    path('empresaRut',empresaRut),
    path('eliminarEmpresa', eliminarEmpresa),
    path('platillo',registroPlatillo),
    path('regin',registroRep),
    path('reginvehiculo',registroVeh),
    path('actTrabajador', actTrabajador)
]
