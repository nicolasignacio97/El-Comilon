from django.urls import path
from administracion.views import administracion
from registroTrabajador.views import registroTrabajador
from registroProveedor.views import registroProveedor
from RegEmpConv.views import registroEmpresa
from RegisterPlatillo.views import registroPlatillo
from RegisterRepartidor.views import registroVeh,registroRep,editRepartidor,deleterepartidor,listarRep

url_patterns = [
    path('',administracion),
    path('trabajador',registroTrabajador),
    path('proveedor',registroProveedor),
    path('empresa',registroEmpresa),
    path('platillo',registroPlatillo),
    path('platillo',registroPlatillo),
    path('regin',registroRep),
    path('reginvehiculo',registroVeh)



]
