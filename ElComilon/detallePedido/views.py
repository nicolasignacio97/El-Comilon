import base64

from django.shortcuts import get_object_or_404, redirect, render
from django.db import connection
from core.models import Pedido, DetallePedido, Cliente
from django.contrib.auth.models import User

# Create your views here.
# def listadoPedidos(request):
#     data = {
#         'pedidos':listarPedidos()
#     }
    
#     return render(request, 'detallePedido.html', data)

def detallePedido(request, idpedido, id):
    cliente = get_object_or_404( User, id = id)
    data = {
        'pedido':listarPedidos(idpedido),
        'platillos':listado_platillos(idpedido),
        'cliente': cliente
    }
    return render(request,'detallePedido.html', data)
    


def listarPedidos(idpedido):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("VER_PEDIDO", [idpedido, out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def listado_platillos(idpedido):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("VER_PEDIDO", [idpedido, out_cur])    

    lista = []
    for fila in out_cur:
        data = {
            'data':fila
        }
        lista.append(data)

    return lista