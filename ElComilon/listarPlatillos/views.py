from django.shortcuts import get_object_or_404, redirect, render
from django.db import connection
import base64
import cx_Oracle
from core.models import Platillo
from django.contrib import messages

# Create your views here.
def listarPlatillos(request):
    data = {
        'platillos':listado_platillos()
    }
    return render(request, 'listarPlatillos.html', data)

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


def eliminarPlatillo(request, id):
    platillo = get_object_or_404(Platillo, idplatillo=id)
    platillo.delete()
    messages.success(request, "Se ha eliminado correctamente el platillo "+ platillo.nombre)
    return redirect(to="/administracion/listarPlatillos")

