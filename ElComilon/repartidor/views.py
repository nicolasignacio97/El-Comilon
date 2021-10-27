from typing import List
from django.shortcuts import get_object_or_404, render, redirect
from django.db import connection
import cx_Oracle


# Create your views here.

def viewRepartidor(request):
    # print(listado_pedidos_reparto())
    dataRep = {
        'repartos':listado_pedidos_reparto()
    }
    return render(request,'viewRepartidor.html', dataRep)


def listado_pedidos_reparto():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LIST_PEDIDOS_REPARTO", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista


#MODIFICAR ESTADO REPARTO
def modificar_cliente_convenio():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_MODIFICAR_CLIENTE_CONVENIO',[rutcliente, nomUsuario , nombres, apellidos, direccion, contrasena,telefono,correo, saldocli,rutempcli,salida])
    return salida.getvalue()
