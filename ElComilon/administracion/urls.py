from os import name
from django.urls import path
from django.urls.conf import include

from administracion.views import administracion
from registroTrabajador.views import registroTrabajador
from RegEmpConv.views import registroEmpresa
from RegisterPlatillo.views import registroPlatillo
from listarPlatillos.views import listarPlatillos, eliminarPlatillo, platilloNombre
from actualizarPlatillo.views import modificarPlatillo
from django.contrib.auth.decorators import login_required
from RegCliConv.views import RegistroCliConvenio,cleanRutcliente, listarCliConv, modificarCliConv, eliminarCliConv

from registroTrabajador.views import listaTrabajador
from RegEmpConv.views import listaEmpresa
from RegEmpConv.views import empresaRut
from RegEmpConv.views import eliminarEmpresa,clean_rut_emp_convenio
from gestionRestaurantes.views import listarRestaurantes, modificarRepreResta, EliminarRepreResta,registroProveedor
from registroTrabajador.views import actTrabajador,actualizarTrabajador,trabajadorRut,eliminarTrabajador,clean_rut_trabajador
from RegEmpConv.views import actualizarEmpresa, actEmpresa
from RegisterRepartidor.views import registroVeh, Registrorep, editRepartidor, deleterepartidor, listarRep, clean_rut,clean_patente

url_patterns = [
    path('', administracion),
    path('trabajador/', registroTrabajador, name='trabajador'),
    path('valruttrabajador', clean_rut_trabajador, name='cleanruttrabajador'),
    path('proveedor', registroProveedor, name='proveedor'),
    path('empresa', registroEmpresa, name='empresa'),
    path('valrutempresa', clean_rut_emp_convenio, name='cleanrutempresa'),
    path('platillo', registroPlatillo, name='platillo'),
    path('modificarPlatillo/<id>/', modificarPlatillo, name='modificarPlatillo'),
    path('eliminarPlatillo/<id>', eliminarPlatillo, name='eliminarPlatillo'),
    path('listarPlatillos', listarPlatillos, name='listarPlatillos'),
    path('platilloNombre', platilloNombre, name='platilloNombre'),
    path('ClienteConvenio', RegistroCliConvenio, name='ClienteConvenio'),
    path('valrutcliente', cleanRutcliente, name='valrutcliente'),
    path('listarCliConv', listarCliConv, name='listarCliConv'),
    path('modCliConv/<id>', modificarCliConv, name='modCliConv'),
    path('eliminar/<rutcliente>/<id>', eliminarCliConv, name='eliminarCliente'),
    path('listaTrabajador', listaTrabajador, name='listaTrabajador'),
    path('trabajadorRut', trabajadorRut, name='trabajadorRut'),
    path('actualizarTrabajador', actualizarTrabajador,name='actualizarTrabajador'),
    path('eliminarTrabajador/<ruttrabajador>/<id>/', eliminarTrabajador, name='eliminarTrabajador'),
    path('listaEmpresa', listaEmpresa, name='listaEmpresa'),
    path('empresaRut', empresaRut, name='empresaRut'),
    path('eliminarEmpresa', eliminarEmpresa, name='eliminarEmpresa'),
    path('platillo', registroPlatillo, name='platillo'),
    path('listarProveedores', listarRestaurantes, name="listarProveedores"),
    path('modificarProveedor/<id>/<id2>',modificarRepreResta, name='modificarProveedor'),
    path('eliminarProveedor/<id>/<id2>/',EliminarRepreResta, name='eliminarProveedor'),
    path('restauranteRut', restauranteRut, name='restauranteRut'),
    path('regin/', Registrorep, name='regin'),
    path('listarep', listarRep, name="listarep"),
    path('updaterepartidor/<rutrepartidor>/',editRepartidor, name='updrpartidor'),
    path('deleterepartidor/<rutrepartidor>/<id>/',deleterepartidor, name='deleterepartidor'),
    path('actualizarEmpresa', actualizarEmpresa),
    path('actEmpresa', actEmpresa),
    path('empresaRut', empresaRut, name='empresaRut'),
    path('eliminarEmpresa', eliminarEmpresa, name='eliminarEmpresa'),
    path('platillo', registroPlatillo, name='platillo'),
    path('reginvehiculo', registroVeh, name='reginvehiculo'),
    path('actTrabajador', actTrabajador, name='actTrabajador'),
    path('valrut', clean_rut, name='validarRut'),
    path('cleanpatente', clean_patente, name='Cleanpatente'),
]
