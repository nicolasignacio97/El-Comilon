from django.shortcuts import get_object_or_404, redirect, render
from django.db import connection
import cx_Oracle
import base64
from core.models import Platillo
from django.contrib import messages


# Create your views here.
def actualizarPlatillo(request):
    data = {
        'platillos':listado_platillos(),
        'Restaurante':listarRestaurante()
    }
    
    return render(request, 'actualizarPlatillo.html', data)

def listado_platillos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PLATILLOS", [out_cur])    

    lista = []
    for fila in out_cur:
        data = {
            'data':fila,
            'imagen':str(base64.b64encode(fila[4].read()), 'utf-8')
        }
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
    platillo = get_object_or_404(Platillo, idplatillo=id)
    dataMod = {
        'seleccion': platillo
    }
    if request.method == 'POST':
        nombrePlatillo = request.POST.get('Nombre').upper()
        ingredientes = request.POST.get('Ingredientes').upper()
        valor = request.POST.get('Valor')
        foto = request.FILES['foto'].read()
        ModificarPlatillo(id,nombrePlatillo, ingredientes, valor, foto)
        messages.success(request, "Se ha modificado correctamente el platillo "+ platillo.nombre)
        return redirect(to="/administracion/listarPlatillos")

 
    return render(request, 'actualizarPlatillo.html', dataMod)

def ModificarPlatillo(idPlatillo, nomPlatillo, ingPlatillo,valPlatillo, fotPlatillo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("ACTUALIZAR_PLATILLO", [idPlatillo, nomPlatillo,ingPlatillo, valPlatillo, fotPlatillo, salida])
    return salida.getvalue()