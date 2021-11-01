from django.shortcuts import get_object_or_404, redirect, render
from django.db import connection
import cx_Oracle
import base64
from core.models import Platillo
from django.contrib import messages


# Create your views here.
def actualizarPlatillo(request, id):
    data = {
        'platillos':listado_platillos(id),
        'Restaurante':listarRestaurante()
    }
    
    return render(request, 'actualizarPlatillo.html', data)

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

def modificarPlatillo(request, id):
    dataMod = {
        'platillo':listado_platillos(id),
        'foto':listado_fotos(id)
    }
    if request.method == 'POST':
        nombrePlatillo = request.POST.get('Nombre').upper()
        ingredientes = request.POST.get('Ingredientes').upper()
        valor = request.POST.get('Valor')
        foto = request.FILES['foto'].read()            
        ModificarPlatillo(id,nombrePlatillo, ingredientes, valor, foto)
        messages.success(request, "Se ha modificado correctamente el platillo ")
        return redirect(to="/administracion/listarPlatillos")

 
    return render(request, 'actualizarPlatillo.html', dataMod)

def ModificarPlatillo(idPlatillo, nomPlatillo, ingPlatillo,valPlatillo, fotPlatillo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("ACTUALIZAR_PLATILLO", [idPlatillo, nomPlatillo,ingPlatillo, valPlatillo, fotPlatillo, salida])
    return salida.getvalue()