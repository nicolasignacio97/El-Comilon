from django.shortcuts import get_object_or_404, render, redirect
from .forms import EditarUsuario, EditarRecepcionista
from django.contrib.auth.models import User
from django.contrib import messages
from core.models import Trabajador,Pedido
from django.db import connection
import cx_Oracle

# Create your views here.

def viewRecepcionista(request):
    dataRep = {
        'listos':listado_pedidos_listos(),
        'TotalPedidos':len(listado_pedidos_listos())
    }
    return render(request,'viewRecepcionista.html',dataRep)

#CAMBIAR ESTADO DE PEDIDOS
def cambiarEstado(request,id):
    pedido = get_object_or_404(Pedido,idpedido=id)
    dataMod = {
       'pedidoSelect' : pedido,
       'estados': listado_estados_pedido(), 
       'TotalPedidos':len(listado_pedidos_listos())
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
       'repartidores': listado_repartidores_dispo(),
       'TotalPedidos':len(listado_pedidos_listos())
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



def menuRecepcion(request, id):
    usuario = get_object_or_404(User, id=id)
    trabajador = get_object_or_404(Trabajador, idcuenta=id)
    formCuenta = EditarUsuario(instance=usuario)
    formPersonal = EditarRecepcionista(instance=trabajador)
    data= {
        'usuario': usuario,
        'formCuenta': formCuenta,
        'trabajador': trabajador,
        'form': formPersonal,
        'TotalPedidos':len(listado_pedidos_listos())
    }
    if request.method == 'POST':
        formCuenta = EditarUsuario(request.POST, instance=request.user)
        formPersonal = EditarRecepcionista(request.POST, instance=trabajador)
    if formCuenta.is_valid():
        if formPersonal.is_valid():
            formCuenta.save()
            formPersonal.save()
            messages.success(request, " Modificado correctamente")
            usuario = get_object_or_404(User, id=id)
            trabajador = get_object_or_404(Trabajador, idcuenta=id)
            formCuenta = EditarUsuario(instance=usuario)
            formPersonal = EditarRecepcionista(instance=trabajador)
            data2= {
                'usuario': usuario,
                'formCuenta': formCuenta,
                'trabajador': trabajador,
                'form': formPersonal,
                'TotalPedidos':len(listado_pedidos_listos())
            }
            return render (request, 'menuRecepcionista.html',data2)

    return render (request, 'menuRecepcionista.html',data)

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
