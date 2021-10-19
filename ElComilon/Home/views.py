from django.shortcuts import render
from django.db import connection
import cx_Oracle
from django.core.files.base import ContentFile
import base64

# Create your views here.


def inicio(request):
    data = {
        'platillos': listarPlatillos()
    }
    return render(request, 'Home/index.html', data)


def quienesSomos(request):
    return render(request, 'quienes-somos.html')


def listarPlatillos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PLATILLOS", [out_cur])
    lista = []

    for i in out_cur:
        if i != None:
            data = {
                'data': i,
                'imagen': str(base64.b64encode(i[4].read()), 'utf-8')
            }
        lista.append(data)

    return lista