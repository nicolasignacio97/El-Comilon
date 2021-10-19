from django.shortcuts import render
from django.db import connection
import cx_Oracle

# Create your views here.
def reclamo(request):
    data = {

    }

    if request.method == 'POST':
        rutcliente = '1'
        descReclamo = request.POST.get('descReclamo')
        salida = agregar_reclamo(descReclamo,rutcliente)
        if salida == 1:
            data['mensaje'] = 'AGREGADO CORRECTAMENTE'
        else:
            data['mensaje'] = 'UPS, NO SE HA PODIDO AGREGAR'

    return render(request,'reclamoUser.html', data)


def agregar_reclamo(descReclamo, rutcliente):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_RECLAMO',[descReclamo,rutcliente, salida])
    return salida.getvalue()