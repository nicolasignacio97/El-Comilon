from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db import connection
import base64
from core.models import Cliente,MenuSemanal
import cx_Oracle

# Create your views here.


def crearMenu (request,id):
    cliente =  get_object_or_404(Cliente,idcuenta = id)
    
    data = {
        'menu':listado_menu(cliente.rutcliente),
        'platillos':listado_platillos(),
        'cliente':cliente
    }
  
    if request.method == 'POST':
        dia = request.POST.get('dia')
        idplatillo = request.POST.get('platillo')
        rut = cliente.rutcliente

        eliminarMenu(dia,rut)
        registrarMenu(dia,idplatillo, rut)
        data = {
            'menu':listado_menu(cliente.rutcliente),
            'platillos':listado_platillos(),
            'cliente':cliente
        }
        return render(request, 'menu.html', data)
    return render(request, 'menu.html', data)

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

def registrarMenu(dia,idplatillo, rut):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    cursor.callproc("SP_INSERT_MENU",[dia,idplatillo, rut])
    return 0

def eliminarMenu(dia, rut):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    cursor.callproc("SP_ELIMINAR_MENU",[dia, rut])
    return 0


def listado_menu(rut):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_MENU", [rut,out_cur])    

    lista = []
    for fila in out_cur:
        data = {
            'data':fila
        }
        lista.append(data)

    return lista