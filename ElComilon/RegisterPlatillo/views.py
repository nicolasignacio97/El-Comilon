from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.http.response import Http404
from django.contrib import messages
from core.models import Platillo
from django.db import connection
import base64
import cx_Oracle

@permission_required('core')
def registroPlatillo (request):
    data = {
    'Restaurante':listarRestaurante()
}
    if request.method == 'POST':
        nombrePlatillo = request.POST.get('Nombre').upper()
        ingredientes = request.POST.get('Ingredientes').upper()
        valor = request.POST.get('Valor')
        foto = request.FILES['foto'].read()
        rutRestaurante = request.POST.get('restaurante')
        check1 = request.POST.get('Disponible')
        if check1:
            disponible = 1
        else:
            disponible = 0
        registrarPlatillo(nombrePlatillo, ingredientes, valor, foto, rutRestaurante, disponible)
        messages.success(request, "Se ha creado correctamente el platillo "+nombrePlatillo)
        return redirect(to="/administracion/listarPlatillos")
    return render(request,'registrarPlatillo.html', data)


def listarRestaurante():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_RESTAURANT", [out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def registrarPlatillo(nomPlatillo, ingPlatillo, valPlatillo, fotPlatillo, rutRest, dispo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("INSERTAR_PLATILLO", [nomPlatillo, ingPlatillo, valPlatillo, fotPlatillo, rutRest, dispo, salida]) 
    return salida.getvalue()


# Create your views here.

@permission_required('core')
def modificarPlatillo(request, id):
    platillo = get_object_or_404(Platillo, idplatillo=id)
    dataMod = {
        'platillo':listado_platillos(id),
        'foto':listado_fotos(id)
    }
    if request.method == 'POST':
        nombrePlatillo = request.POST.get('Nombre').upper()
        ingredientes = request.POST.get('Ingredientes').upper()
        valor = request.POST.get('Valor')
        checkDisponible = request.POST.get('Disponible')
        checkStock = request.POST.get('Stock')
        if checkDisponible:
            disponible = 1
        else:
            disponible = 0

        if checkStock:
            stock = 1
        else:
            stock = 0
        if 'foto' in request.POST:
         foto = False
         ModificarPlatilloSinFoto(id,nombrePlatillo, ingredientes, valor,disponible, stock)
        else:
         foto = True
         foto = request.FILES['foto'].read()
         ModificarPlatillo(id,nombrePlatillo, ingredientes, valor, foto,disponible, stock)
        messages.success(request, "Se ha modificado correctamente el platillo "+ platillo.nombre)
        return redirect(to="/administracion/listarPlatillos")
    return render(request, 'actualizarPlatillo.html', dataMod)

def listado_platillos(id):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("VER_PLATILLO", [id, out_cur])    

    lista = []
    for fila in out_cur:
         lista.append(fila)

    return lista

def listado_fotos(id):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("VER_PLATILLO", [id, out_cur])    

    lista = []
    for fila in out_cur:
        data = str(base64.b64encode(fila[3].read()), 'utf-8')
        lista.append(data)

    return lista

def listarRestaurante():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_RESTAURANT", [out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def ModificarPlatillo(idPlatillo, nomPlatillo, ingPlatillo,valPlatillo, fotPlatillo, disponible, stock):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("ACTUALIZAR_PLATILLO", [idPlatillo, nomPlatillo,ingPlatillo, valPlatillo, fotPlatillo, disponible, stock,salida])
    return salida.getvalue()

def ModificarPlatilloSinFoto(idPlatillo, nomPlatillo, ingPlatillo,valPlatillo, disponible, stock):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("ACTUALIZAR_PLATILLO_SIN_FOTO", [idPlatillo, nomPlatillo,ingPlatillo, valPlatillo, disponible, stock, salida])

    return salida.getvalue()


# Create your views here.
data = {}
@permission_required('core')
def listarPlatillos(request):
    global data
    page = request.GET.get('page',1)
    Lista = listado_platillos()
    try:
        paginator = Paginator(Lista, 10)
        Lista = paginator.page(page)
    except :
        raise Http404

    data = {
        'entity': Lista,
        'paginator' : paginator,
    }
    return render(request, 'listarPlatillos.html', data)


def listado_platillos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PLATILLOS_ADMIN", [out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

@permission_required('core')
def eliminarPlatillo(request, id):
    platillo = get_object_or_404(Platillo, idplatillo=id)
    platillo.delete()
    messages.success(request, "Se ha eliminado correctamente el platillo "+ platillo.nombre)
    return redirect(to="/administracion/listarPlatillos")


@permission_required('core')
def platilloNombre(request):
    global data
    if request.method == 'POST':

        nombre = request.POST.get('nombrePlatillo').upper()

        data = {
        'entity': listarPlatilloNombre(nombre)   
        }
    return render(request, 'listarPlatillos.html', data)


def listarPlatilloNombre(nombre):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PLATILLOS_NOMBRE", [nombre, out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista
