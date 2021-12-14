from django.contrib import messages
from core.models import Repartidor, Pedido, Vehiculo
from django.contrib.auth.models import User
from .forms import EditarRepartidor, EditarUsuario, EditarVehiculo
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import permission_required
from django.db import connection
import cx_Oracle

def cambiarEstadoTiendaRepartidor(request, id):
    modificar_estado_pedido(id, 5)
    return redirect(to='repartidor')


# Create your views here.
@permission_required('core.view_pedido')
def viewRepartidor(request):
    # print(listado_pedidos_reparto())
    dataRep = {
        'repartos': listado_pedidos_reparto(),
        'TotalPedidos':len(listado_pedidos_reparto())
    }
    return render(request, 'viewRepartidor.html', dataRep)


@permission_required('core.view_pedido')
def viewPedido(request, id):
    pedido = get_object_or_404(Pedido, idpedido=id)
    dataMod = {
        'pedidoSelect': pedido 
    }
    return render(request, 'viewPedido.html', dataMod)

@permission_required('core.view_pedido')
def PerfilRepartidor(request, id):
    usuario = get_object_or_404(User, id=id)
    repartidor = get_object_or_404(Repartidor, idcuenta=id)

    formCuenta = EditarUsuario(instance=usuario)
    formPersonal = EditarRepartidor(instance=repartidor)
    data = {
        'usuario': usuario,
        'formCuenta': formCuenta,
        'repartidor': repartidor,
        'form': formPersonal,
        'TotalPedidos':len(listado_pedidos_reparto())
    }
    if request.method == 'POST':
        formCuenta = EditarUsuario(request.POST, instance=request.user)
        formPersonal = EditarRepartidor(request.POST, instance=repartidor)
    if formCuenta.is_valid():
        if formPersonal.is_valid():
            formCuenta.save()
            formPersonal.save()
            messages.success(request, " Modificado correctamente")
            usuario = get_object_or_404(User, id=id)
            repartidor = get_object_or_404(Repartidor, idcuenta=id)
            formCuenta = EditarUsuario(instance=usuario)
            formPersonal = EditarRepartidor(instance=repartidor)
            data2 = {
                'usuario': usuario,
                'formCuenta': formCuenta,
                'repartidor': repartidor,
                'form': formPersonal,
                'TotalPedidos':len(listado_pedidos_reparto())
            }
            return render(request, 'repartidorPerfil.html', data2)
    return render(request, 'repartidorPerfil.html', data)

@permission_required('core.view_pedido')
def MiVehiculo(request, id):
    repartidor = get_object_or_404(Repartidor, idcuenta=id)
    vehiculo = get_object_or_404(Vehiculo, rutrepartidor=repartidor.rutrepartidor)
    formVehiculo = EditarVehiculo(instance=vehiculo)
    data = {
        'vehiculo': vehiculo,
        'form': formVehiculo,
        'TotalPedidos':len(listado_pedidos_reparto())
    }
    if request.method == 'POST':
        formvehiculo = EditarVehiculo(request.POST, instance=vehiculo)
        if formvehiculo.is_valid():
            formvehiculo.save()
            messages.success(request, " Modificado correctamente")
            vehiculo = get_object_or_404(
                Vehiculo, rutrepartidor=repartidor.rutrepartidor)
            formVehiculo = EditarVehiculo(instance=vehiculo)
            data2 = {
                'vehiculo': vehiculo,
                'form': formVehiculo
            }
            return render(request, 'miVehiculo.html', data2)

    return render(request, 'miVehiculo.html', data)


def listado_pedidos_reparto():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LIST_PEDIDOS_REPARTO", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista


# MODIFICAR ESTADO REPARTO
def modificar_estado_pedido(idpedido, idestpedido):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_MODIFICAR_ESTADO_REPARTO', [
                    idpedido, idestpedido, salida])
    return salida.getvalue()
