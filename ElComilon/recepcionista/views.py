from django.shortcuts import render
from django.contrib import messages
from typing import List
from django.shortcuts import get_object_or_404, render, redirect
from django.db import connection
import cx_Oracle

from core.models import Pedido

# Create your views here.

def viewRecepcionista(request):
    dataRep = {
        'listos':listado_pedidos_listos(),
    }

    return render(request,'viewRecepcionista.html',dataRep)

#CAMBIAR ESTADO DE PEDIDOS
def cambiarEstado(request,id):
    pedido = get_object_or_404(Pedido,idpedido=id)
    dataMod = {
       'pedidoSelect' : pedido,
       'estados': listado_estados_pedido()     
    }

    if request.method == 'POST':
        idpedido = id
        idestpedido = request.POST.get('estado_pedido')
        salida = cambiar_estado(idpedido, idestpedido)
        if salida == 1:
            return redirect(to="recepcionista")
        else:
            dataMod['mensaje'] = 'UPS, NO SE HA PODIDO CAMBIAR ESTADO PEDIDO'

    return render(request, 'cambioEstado.html',dataMod)


#ASIGNAR REPARTIDOR A PEDIDO
def asignarRepartidor(request,id):
    pedido = get_object_or_404(Pedido,idpedido=id)
    dataMod = {
       'pedidoSelect' : pedido,
       'repartidores': listado_repartidores_dispo()     
    }

    if request.method == 'POST':
      
        idestpedido = 4
        rutrepartidor = request.POST.get('repartidor')
        salida = asignar_repartidor(id, idestpedido, rutrepartidor)
        
        if salida == 1:
            return redirect(to="recepcionista")
        else:
            dataMod['mensaje'] = 'UPS, NO SE HA PODIDO ASIGNAR UN REPARTIDOR EL PEDIDO'
    return render(request,'asignaRepartidor.html',dataMod)


def listado_pedidos_listos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LIST_PEDIDOS_LISTOS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def listado_estados_pedido():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LIST_ESTADO_PEDIDO", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def listado_repartidores_dispo():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LIST_REPARTIDORES_DISPO", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def cambiar_estado(idpedido, idestpedido):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_MODIFICAR_ESTADO_PEDIDO',[idpedido, idestpedido,salida])
    return salida.getvalue()
    
def asignar_repartidor(id, idestpedido,rutrepartidor):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_MODIFICAR_ASIGNAR_REPARTIDOR',[id, idestpedido,rutrepartidor ,salida])
    return salida.getvalue()
