from django.shortcuts import render
from django.db import connection
import base64

# Create your views here.
def platillos(request):
    data = {
        'platillos':listado_platillos()
    }
    return render(request, 'platillos.html', data)

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