from django.shortcuts import render
from django.db import connection
import cx_Oracle

# Create your views here.

def registroProveedor (request):
    data = {
        
    }
    if request.method == 'POST':
        
        # REPRESENTANTE
        rutRepre = request.POST.get('representante').upper()
        nombresRepre = request.POST.get('nombresRepresentante').upper()
        apellidosRepre = request.POST.get('apellidos').upper()
        telefono = request.POST.get('telefono')
        correo = request.POST.get('email')
        
        salidaRepre = registrarRepre(rutRepre,nombresRepre,apellidosRepre,telefono,correo)

        # RESTAURANTE PROVEEDOR
        rutRest = request.POST.get('rutRestaurante').upper()
        nombre = request.POST.get('nombre').upper()
        direccion = request.POST.get('direccion').upper()
        representante =  request.POST.get('representante').upper()
        tipo = 1
        salidaPrve = registrarProve(rutRest,nombre,direccion,representante,tipo)

        # SALIDA REPRESENTANTE
        if salidaRepre == 1 :
            data['mensaje'] = 'Agregado correctamente'
        else:
            data['mensaje'] = 'No se ha podido guardar'

        # SALIDA RESTAURANTE PROVEEDOR
        if salidaPrve == 1 :
            data['mensaje'] = 'Agregado correctamente'
        else:
            data['mensaje'] = 'No se ha podido guardar'

    #SALIDA PAGINA
    return render (request,'registro-proveedor.html',data)

# REPRESENTANTE
def registrarRepre(rutRepre,nombresRepre,apellidosRepre,telefono,correo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salidaRepre = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("REGISTRAR_REPRESENTANTE",[rutRepre,nombresRepre,apellidosRepre,telefono,correo, salidaRepre])
    return salidaRepre.getvalue()

# RESTAURANTE PROVEEDOR
def registrarProve(rutRest, nombreRest, direccionRest, rutRepresentante, idTipo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salidaPrve = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("REGISTRAR_PROVEEDOR",[rutRest, nombreRest, direccionRest, rutRepresentante, idTipo, salidaPrve])
    return salidaPrve.getvalue()

    


