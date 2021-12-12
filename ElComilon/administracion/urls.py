from os import name
from django.urls import path
from django.urls.conf import include

from administracion.views import administracion
from RegEmpConv.views import registroEmpresa
from RegisterPlatillo.views import registroPlatillo
from listarPlatillos.views import listarPlatillos, eliminarPlatillo, platilloNombre
from actualizarPlatillo.views import modificarPlatillo

from RegCliConv.views import RegistroCliConvenio,cleanRutcliente, listarCliConv, modificarCliConv, eliminarCliConv, cliConvRut,actualizarSaldo
from RegEmpConv.views import EliminarEmpresa,clean_rut_emp_convenio,empresaRut,listaEmpresa
from gestionRestaurantes.views import listarRestaurantes, modificarRepreResta, EliminarRepreResta,registroProveedor, restauranteRut

from registroTrabajador.views import actualizarTrabajador,trabajadorRut,eliminarTrabajador,clean_rut_trabajador,listaTrabajador,registroTrabajador

from RegEmpConv.views import actualizarEmpresa, actEmpresa
from RegisterRepartidor.views import Registrorep, editRepartidor, deleterepartidor, listarRep, clean_rut,clean_patente, repartidorRut

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
    path('cliConvRut', cliConvRut, name='cliConvRut'),
    path('actualizarSaldo', actualizarSaldo, name='actualizarSaldo'),
    path('modCliConv/<id>', modificarCliConv, name='modCliConv'),
    path('eliminar/<rutcliente>/<id>', eliminarCliConv, name='eliminarCliente'),
    path('listaTrabajador', listaTrabajador, name='listaTrabajador'),
    path('trabajadorRut', trabajadorRut, name='trabajadorRut'),
    
    path('actualizarTrabajador/<id>', actualizarTrabajador,name='actualizarTrabajador'),
    path('eliminarTrabajador/<rut>', eliminarTrabajador, name='eliminarTrabajador'),
    path('listaEmpresa', listaEmpresa, name='listaEmpresa'),
    path('empresaRut', empresaRut, name='empresaRut'),
   
    path('eliminarEmpresa/<id>', EliminarEmpresa, name='eliminarEmpresa'),
    path('platillo', registroPlatillo, name='platillo'),
    path('listarProveedores', listarRestaurantes, name="listarProveedores"),
    path('modificarProveedor/<id>/<id2>',modificarRepreResta, name='modificarProveedor'),
    path('eliminarProveedor/<id>/<id2>/',EliminarRepreResta, name='eliminarProveedor'),
    path('restauranteRut', restauranteRut, name='restauranteRut'),
    path('regin/', Registrorep, name='regin'),
    path('listarep', listarRep, name="listarep"),
    path('repartidorRut', repartidorRut, name='repartidorRut'),
    path('updaterepartidor/<rutrepartidor>/',editRepartidor, name='updrpartidor'),
    path('deleterepartidor/<rutrepartidor>',deleterepartidor, name='deleterepartidor'),
    path('actualizarEmpresa', actualizarEmpresa),
    path('actEmpresa', actEmpresa),
    path('empresaRut', empresaRut, name='empresaRut'),
    path('platillo', registroPlatillo, name='platillo'),


    path('valrut', clean_rut, name='validarRut'),
    path('cleanpatente', clean_patente, name='Cleanpatente'),
]
