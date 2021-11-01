from django.http import request
from django.shortcuts import render
from django.db import connection, reset_queries
from django.contrib.auth.decorators import permission_required
import cx_Oracle

# Create your views here.

@permission_required('core')
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

        salida = registrarTrabajador(rutTrabajador, nombres, apellidos,
                                     fechaContrato, usuario, contrasena, rutRestaurante, idCargo)

        if salida == 1:
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

@permission_required('core')
def registrarTrabajador(rutTrabajador, nombres, apellidos, fechaContrato, usuario, contrasena, rutRestaurante, idCargo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salidaPrve = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("REGISTRAR_TRABAJADOR", [rutTrabajador, nombres, apellidos,
                    fechaContrato, usuario, contrasena, rutRestaurante, idCargo, salidaPrve])
    return salidaPrve.getvalue()

@permission_required('core')
def listaTrabajador(request):
    data = {
        'trabajadores': listarTrabajador()
    }
    return render(request, 'listarTrabajador.html', data)


def listarTrabajador():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_TRABAJADORES", [out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

@permission_required('core')
def trabajadorRut(request):
    if request.method == 'POST':

        rut = request.POST.get('trabajadorRut')

        data = {
        'trabajadores': listarTrabajadorRut(rut)
        }
    return render(request, 'listarTrabajador.html', data)


def listarTrabajadorRut(rut):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_TRABAJADORES_RUT", [rut, out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista
@permission_required('core')
def actualizarTrabajador(request):

    if request.method == 'POST':

        rut = request.POST.get('btnActualizar')

        data = {
        'trabajador': listarTrabajadorRut(rut),
        'cargo': listar()
        }

 
    return render(request, 'actualizarTrabajador.html', data)
    
@permission_required('core')
def actTrabajador(request):
    if request.method =='POST':
        rutTrabajador = request.POST.get('rutTrabajador').upper()
        nombres = request.POST.get('nombres').upper()
        apellidos = request.POST.get('apellidos').upper()
        usuario = request.POST.get('nombreU')
        idCargo = request.POST.get('cargo')

        actualizar(rutTrabajador, nombres, apellidos, usuario, idCargo)

    return listaTrabajador(request)

def actualizar(rutTrabajador, nombres, apellidos, usuario, idCargo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    cursor.callproc("SP_ACT_TRABAJADOR", [rutTrabajador, nombres, apellidos, usuario, idCargo])

    return 0

def eliminarTrabajador(request):
    if request.method == 'POST':
        rut = request.POST.get('btnEliminar')
    
    eliminar(rut)

    return listaTrabajador(request)

def eliminar(rut):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()

    cursor.callproc("SP_ELIMINAR_TRABAJADOR", [rut])

    return 0