from typing import List
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import permission_required
from django.db import connection
import cx_Oracle

from core.models import Pedido


# Create your views here.
@permission_required('core.view_pedido')
def viewRepartidor(request):
    # print(listado_pedidos_reparto())
    dataRep = {
        'repartos':listado_pedidos_reparto()
    }

    
    return render(request,'viewRepartidor.html', dataRep)

@permission_required('core.view_pedido')
def viewPedido(request,id):
    pedido = get_object_or_404(Pedido,idpedido=id)
    dataMod = {
       'pedidoSelect' : pedido
    }

    if request.method == 'POST':
        idestpedido = 5
        salida = modificar_estado_pedido(id, idestpedido)
        if salida == 1:
            return redirect(to="/repartidor")
        else:
            dataMod['mensaje'] = 'UPS, NO SE HA PODIDO FINALIZAR EL PEDIDO'
    return render(request,'viewPedido.html',dataMod)


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
def modificar_estado_pedido(idpedido, idestpedido):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_MODIFICAR_ESTADO_REPARTO',[idpedido, idestpedido ,salida])
    return salida.getvalue()
