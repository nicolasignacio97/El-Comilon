from django.shortcuts import get_object_or_404, redirect, render
from django.db import connection
import cx_Oracle
import base64
from core.models import Platillo
from django.contrib import messages


# Create your views here.

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