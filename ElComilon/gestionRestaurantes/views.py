from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.db import connection
from core.models import Restaurante, Representante
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required

import cx_Oracle

@permission_required('core')
def listarRestaurantes(request):
    page = request.GET.get('page',1)
    Lista = listado_restaurantes();
    try:
        paginator = Paginator(Lista, 10)
        Lista = paginator.page(page)
    except :
        raise Http404

    data = {
        'entity': Lista,
        'paginator' : paginator,
    }
    return render(request, 'listarRestau_Repre.html', data)

def modificarRepreResta(request, id,id2):
    restaurante = get_object_or_404(Restaurante, rutrestaurante=id)
    representante = get_object_or_404(Representante, rutrepresentante=id2)
    dataMod = {
        'seleccion': restaurante,
        'representante': representante
    }
    if request.method == 'POST':
        rutRest = request.POST.get('rutRestaurante').upper()
        nombre = request.POST.get('nombre').upper()
        direccion = request.POST.get('direccion').upper()

        rutRepre = request.POST.get('representante').upper()
        nombres = request.POST.get('nombresRepresentante').upper()
        apellidos = request.POST.get('apellidos').upper()
        telefono = request.POST.get('telefono').upper()
        correo = request.POST.get('email').upper()
        ModificarProveedor(rutRest, nombre, direccion)
        modificarRepre(rutRepre, nombres, apellidos, telefono, correo)

        messages.success(request, nombre + " Modificado correctamente")
        return redirect(to="/administracion/listarProveedores")
    return render(request, 'modificarProveedor.html', dataMod)

@permission_required('core')
def EliminarRepreResta(request, id, id2):
    restaurante = get_object_or_404(Restaurante, rutrestaurante=id)
    representante = get_object_or_404(Representante, rutrepresentante=id2)
    restaurante.delete()
    representante.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to="/administracion/listarProveedores")

# Create your views here.
@permission_required('core')
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
        
        registrarRepre(rutRepre,nombresRepre,apellidosRepre,telefono,correo)

        # RESTAURANTE PROVEEDOR
        rutRest = request.POST.get('rutRestaurante').upper()
        nombre = request.POST.get('nombre').upper()
        direccion = request.POST.get('direccion').upper()
        representante =  request.POST.get('representante').upper()
        tipo = 2
        registrarProve(rutRest,nombre,direccion,representante,tipo)
        messages.success(request, nombre + " Registrado correctamente")
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

def ModificarProveedor(rutRest, nombreRest, direccionRest):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salidaPrve = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("MODIFICAR_PROVEEDOR", [rutRest, nombreRest, direccionRest, salidaPrve])
    return salidaPrve.getvalue()

def modificarRepre(rutRepre,nombres,apellidos,telefono,correo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salidaPrve = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("MODIFICAR_REPRESENTANTE",[rutRepre,nombres,apellidos,telefono,correo,salidaPrve])
    return salidaPrve.getvalue()

