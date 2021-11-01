from django.urls import path
from django.urls.conf import include
from administracion.views import administracion
from registroTrabajador.views import registroTrabajador
from registroProveedor.views import registroProveedor
from RegEmpConv.views import registroEmpresa
from RegisterPlatillo.views import registroPlatillo
from listarPlatillos.views import listarPlatillos, eliminarPlatillo
from actualizarPlatillo.views import modificarPlatillo
from django.contrib.auth.decorators import  login_required
from RegCliConv.views import RegistroCliConvenio, listarCliConv, modificarCliConv, eliminarCliConv
from RegisterRepartidor.views import registroRep,registroVeh,editRepartidor,listarRep,deleterepartidor
from registroTrabajador.views import listaTrabajador
from registroTrabajador.views import trabajadorRut
from registroTrabajador.views import actualizarTrabajador
from registroTrabajador.views import eliminarTrabajador
from RegEmpConv.views import listaEmpresa
from RegEmpConv.views import empresaRut
from RegEmpConv.views import eliminarEmpresa
from RegisterRepartidor.views import registroVeh, registroRep, editRepartidor, deleterepartidor, listarRep,editvehiculo
from gestionRestaurantes.views import listarRestaurantes, modificarRepreResta,EliminarRepreResta
from RegisterRepartidor.views import registroVeh,registroRep,editRepartidor,deleterepartidor,listarRep
from recepcionista.views import viewRecepcionista, asignarRepartidor

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
    path('recepcionista',viewRecepcionista, name='recepcionista'),
    path('asignacion/<id>', asignarRepartidor, name='asignacionRepartidor'),
    path('listaTrabajador',listaTrabajador),
    path('trabajadorRut',trabajadorRut),
    path('actualizarTrabajador', actualizarTrabajador),
    path('eliminarTrabajador',eliminarTrabajador),
    path('listaEmpresa', listaEmpresa),
    path('empresaRut',empresaRut),
    path('eliminarEmpresa', eliminarEmpresa),
    path('platillo',registroPlatillo),
    path('regin',registroRep),
    path('reginvehiculo',registroVeh)
]

