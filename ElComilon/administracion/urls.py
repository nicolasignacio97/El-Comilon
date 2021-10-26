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
from registroTrabajador.views import actTrabajador

url_patterns = [
    path('', administracion),
    
    path('trabajador',registroTrabajador,name = 'trabajador'),
    path('proveedor', registroProveedor,name = 'proveedor'),
    path('empresa', registroEmpresa,name = 'empresa'),
    path('platillo', registroPlatillo,name = 'platillo'),
    path('modificarPlatillo/<id>/', modificarPlatillo,name = 'modificarPlatillo'),
    path('eliminarPlatillo/<id>', eliminarPlatillo,name = 'eliminarPlatillo'),
    path('listarPlatillos', listarPlatillos,name = 'listarPlatillos'),
    path('ClienteConvenio', RegistroCliConvenio,name = 'ClienteConvenio'),
    path('listarCliConv', listarCliConv,name = 'listarCliConv'),
    path('modCliConv/<id>', modificarCliConv,name = 'modCliConv'),
    path('eliminar/<id>', eliminarCliConv),
    path('listaTrabajador', listaTrabajador,name = 'listaTrabajador'),
    path('trabajadorRut', trabajadorRut,name = 'trabajadorRut'),
    path('actualizarTrabajador', actualizarTrabajador,name = 'actualizarTrabajador'),
    path('eliminarTrabajador', eliminarTrabajador,name = 'eliminarTrabajador'),
    path('listaEmpresa', listaEmpresa,name = 'listaEmpresa'),
    path('empresaRut', empresaRut,name = 'empresaRut'),
    path('eliminarEmpresa', eliminarEmpresa,name = 'eliminarEmpresa'),
    path('platillo', registroPlatillo ,name = 'platillo'),  
    path('listarProveedores',listarRestaurantes,name="listarProveedores"),
    path('modificarProveedor/<id>/<id2>', modificarRepreResta,name = 'modificarProveedor'),
    path('eliminarProveedor/<id>/<id2>/', EliminarRepreResta,name = 'eliminarProveedor'),
    path('regin', registroRep,name="regin"),
    path('reginvehiculo', registroVeh,name="reginvehiculo"),
    path('listarep', listarRep,name="listarep"),
    path('updaterepartidor/<rutrepartidor>/',editRepartidor, name = 'updrpartidor'),
    path('updatevehiculo/<rutrepartidor>/',editvehiculo, name = 'updvehiculo'),
    path('deleterepartidor/<rutrepartidor>/',deleterepartidor, name = 'deleterepartidor'), 
    path('empresaRut',empresaRut,name = 'empresaRut'),
    path('eliminarEmpresa', eliminarEmpresa,name = 'eliminarEmpresa'),
    path('platillo',registroPlatillo,name = 'platillo'),
    path('regin',registroRep,name = 'regin'),
    path('reginvehiculo',registroVeh,name = 'reginvehiculo'),
    path('actTrabajador', actTrabajador,name = 'actTrabajador')
]

