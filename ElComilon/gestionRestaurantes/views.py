from django.shortcuts import get_object_or_404, redirect, render
from django.db import connection
from core.models import Restaurante, Representante

import cx_Oracle


def listarRestaurantes(request):
    data = {
        'Restaurante': listado_restaurantes(),
        'Representante': listado_representante(),
    }
    return render(request, 'listarRestau_Repre.html', data)


def listado_restaurantes():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_RESTAURANTE", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista


def listado_representante():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_REPRESENTANTES", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista


def modificarProveedor(request, id):
    restaurante = get_object_or_404(Restaurante, rutrestaurante=id)
    dataMod = {
        'seleccion': restaurante
    }
    if request.method == 'POST':
        rutRest = request.POST.get('rutRestaurante').upper()
        nombre = request.POST.get('nombre').upper()
        direccion = request.POST.get('direccion').upper()
    
        salida= ModificarProveedor(rutRest,nombre,direccion)
        if salida == 1 :
           return redirect(to ="/administracion/listarProveedores")
        else:
            dataMod['mensaje'] = 'No se ha podido modificar'


    return render(request, 'modificarProveedor.html',dataMod)


def ModificarProveedor(rutRest, nombreRest, direccionRest):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salidaPrve = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("MODIFICAR_PROVEEDOR",[rutRest, nombreRest, direccionRest,salidaPrve])
    return salidaPrve.getvalue()


def EliminarProveedor (request, id):
    restaurante = get_object_or_404(Restaurante, rutrestaurante=id)
    restaurante.delete()
    return redirect(to="/administracion/listarProveedores")




# Representante


def ModificarRepresentante (request, id):
    representante = get_object_or_404(Representante,rutrepresentante=id)
    data ={
        'representante' : representante
    }
    if request.method == 'POST':
        rutRepre = request.POST.get('representante').upper()
        nombres = request.POST.get('nombresRepresentante').upper()
        apellidos = request.POST.get('apellidos').upper()
        telefono = request.POST.get('telefono').upper()
        correo = request.POST.get('email').upper()
    
        salida= modificarRepre(rutRepre,nombres,apellidos,telefono,correo)
        if salida == 1 :
           return redirect(to ="/administracion/listarProveedores")
        else:
            data['mensaje'] = 'No se ha podido modificar'


    return render(request,'modificarRepresentante.html',data)

def modificarRepre(rutRepre,nombres,apellidos,telefono,correo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salidaPrve = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("MODIFICAR_REPRESENTANTE",[rutRepre,nombres,apellidos,telefono,correo,salidaPrve])
    return salidaPrve.getvalue()

def EliminarRepresentante (request, id):
    representante = get_object_or_404(Representante, rutrepresentante=id)
    representante.delete()
    return redirect(to="/administracion/listarProveedores")