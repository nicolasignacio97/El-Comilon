from django.shortcuts import render
from django.db import connection
import base64
import cx_Oracle
from core.models import Platillo
# Create your views here.

def menu (request):
    data = {
        'menu':listado_menu()
    } 
    return render(request, 'menuSemanal.html', data)

def crearMenu (request):

    if request.method == 'POST':
        dia = request.POST.get('dia')
        idplatillo = request.POST.get('platillo')
        rut = '8.736.863-0'


        eliminarMenu(dia,rut)
        registrarMenu(dia,idplatillo, rut)

    data = {
        'menu':listado_menu(),
        'platillos':listado_platillos()
    }

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


def listado_menu():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_MENU", [out_cur])    

    lista = []
    for fila in out_cur:
        data = {
            'data':fila
        }
        lista.append(data)

    return lista