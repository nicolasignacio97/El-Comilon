from django.shortcuts import render
from django.db import connection
import cx_Oracle

# Create your views here.

def registroTrabajador(request):
    data = {
        'cargo': listar()
    }
    if request.method == 'POST':
        
        # REPRESENTANTE
        rutTrabajador = request.POST.get('rutTrabajador').upper()
        nombres = request.POST.get('nombres').upper()
        apellidos = request.POST.get('apellidos').upper()
        fechaContrato = request.POST.get('fecha').upper()
        usuario = request.POST.get('nombreU')
        contrasena = request.POST.get('contrasena')
        rutRestaurante = '77.684.154-9'
        idCargo = request.POST.get('cargo')
        
        salida = registrarTrabajador(rutTrabajador,nombres,apellidos,fechaContrato,usuario,contrasena,rutRestaurante,idCargo)

        if salida == 1 :
            data['mensaje'] = 'Agregado correctamente'
        else:
            data['mensaje'] = 'No se ha podido guardar'

    return render(request, 'registroTrabajador.html', data)


def listar():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_CARGO", [out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def registrarTrabajador(rutTrabajador,nombres,apellidos,fechaContrato,usuario,contrasena,rutRestaurante,idCargo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salidaPrve = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("REGISTRAR_TRABAJADOR",[rutTrabajador,nombres,apellidos,fechaContrato,usuario,contrasena,rutRestaurante,idCargo,salidaPrve])
    return salidaPrve.getvalue()