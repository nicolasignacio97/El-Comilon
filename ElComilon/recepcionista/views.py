from django.shortcuts import get_object_or_404, render, redirect

from .forms import EditarUsuario, EditarRecepcionista
from django.contrib.auth.models import User
from django.contrib import messages
from core.models import Trabajador,Pedido, DetallePedido, Cliente,Repartidor, Reclamo
from django.core.mail import send_mail
from django.conf import settings
from django.db import connection
from django.contrib.auth.decorators import permission_required
import cx_Oracle

# Create your views here.
def cambiarEstadoTienda(request, id):
    cambiar_estado(id, 5)
    return redirect(to='/recepcionista')

@permission_required('core.view_reclamo')    
def viewRecepcionista(request):
    dataRep = {
        'listos':listado_pedidos_listos(),
        'totalReclamos':len(listado_reclamos()),
        'TotalPedidos':len(listado_pedidos_listos()),
        'totalTotal':len(listado_reclamos())+len(listado_pedidos_listos())
    }
    return render(request,'viewRecepcionista.html',dataRep)

def cancelarPedidoRecepcionista(request, id):
    cambiar_estado(id, 6)
    url='recepcionista'
    return redirect(to=url)

#CAMBIAR ESTADO DE PEDIDOS
@permission_required('core.view_reclamo')    
def cambiarEstado(request,id):
    pedido = get_object_or_404(Pedido,idpedido=id)
    detallePedido = DetallePedido.objects.filter(idpedido=pedido.idpedido)
    cliente = get_object_or_404(Cliente, rutcliente=pedido.rutcliente)
    print(pedido.idestpedido)
    dataMod = {
       'detallePedido' : detallePedido, 
       'pedidoSelect' : pedido,
       'cliente' : cliente,
       'totalReclamos':len(listado_reclamos()),
       'estados': listado_estados_pedido(), 
       'TotalPedidos':len(listado_pedidos_listos()),
       'totalTotal':len(listado_reclamos())+len(listado_pedidos_listos())
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
@permission_required('core.view_reclamo')    

def asignarRepartidor(request,id):
    pedido = get_object_or_404(Pedido,idpedido=id)
    dataMod = {
       'pedidoSelect' : pedido,
       'repartidores': listado_repartidores_dispo(),
       'totalReclamos':len(listado_reclamos()),
       'TotalPedidos':len(listado_pedidos_listos()),
       'totalTotal':len(listado_reclamos())+len(listado_pedidos_listos())
    }

    if request.method == 'POST':
        idestpedido = 4
        rutrepartidor = request.POST.get('repartidor')
        repartidor = get_object_or_404(Repartidor, rutrepartidor = rutrepartidor )
        asignar_repartidor(id, idestpedido, rutrepartidor)
        messages.success(request,"Pedido Asignado A "+ repartidor.nombres)
        return redirect(to="recepcionista")

    return render(request,'asignaRepartidor.html',dataMod)

@permission_required('core.view_reclamo')    
def menuRecepcion(request, id):
    usuario = get_object_or_404(User, id=id)
    trabajador = get_object_or_404(Trabajador, idcuenta=id)
    formCuenta = EditarUsuario(instance=usuario)
    formPersonal = EditarRecepcionista(instance=trabajador)
    mensaje = ""
    data= {
        'usuario': usuario,
        'formCuenta': formCuenta,
        'trabajador': trabajador,
        'form': formPersonal,
        'totalReclamos':len(listado_reclamos()),
        'TotalPedidos':len(listado_pedidos_listos()),
        'totalTotal':len(listado_reclamos())+len(listado_pedidos_listos())
    }
    if request.method == 'POST':
        formCuenta = EditarUsuario(request.POST, instance=request.user)
        print(formCuenta)
        formPersonal = EditarRecepcionista(request.POST, instance=trabajador)
        # if User.objects.filter(username= formCuenta.username).exists():
        #     mensaje = 'Ya existe un Restaurante con este Nombre de usuario.'
        # else:
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
                        'TotalPedidos':len(listado_pedidos_listos()),
                        'mensaje':mensaje
                    }
                    return render (request, 'menuRecepcionista.html',data2)

    return render (request, 'menuRecepcionista.html',data)

@permission_required('core.view_reclamo')    

def verReclamos(request):
   
    data={
        'reclamos':listado_reclamos(),
        'totalReclamos':len(listado_reclamos()),
        'TotalPedidos':len(listado_pedidos_listos()),
        'totalTotal':len(listado_reclamos())+len(listado_pedidos_listos())
    }
    return render(request,'verReclamos.html',data)
    


@permission_required('core.view_reclamo')    

def detalleReclamo(request, id):
    reclamo = get_object_or_404(Reclamo, idreclamo = id)
    clientes = get_object_or_404(Cliente, rutcliente = reclamo.rutcliente)
    cliente = listado_clientes(clientes.rutcliente)
    user = get_object_or_404 (User, id= cliente[0][11])
    data={
        'reclamo' : reclamo,
        'correo': user.email,
        'totalReclamos':len(listado_reclamos()),
        'clientes':clientes,
        'TotalPedidos':len(listado_pedidos_listos()),
        'totalTotal':len(listado_reclamos())+len(listado_pedidos_listos())
    }
    if request.method=="POST":
        subjet = "Estado de su Reclamo"
        message = request.POST["Mensaje"]
        email_from = settings.EMAIL_HOST_USER
        recipient_list=[user.email]
        send_mail(subjet,message,email_from,recipient_list)
        cambiar_estado_reclamo(id, 2)
        messages.success(request,'Mensaje enviado exitosamente')
        return redirect(to='verReclamos')
 
    return render(request,'detalleReclamo.html',data)



def listado_clientes(rut):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_CLIENTES", [rut, out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

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
    
def cambiar_estado_reclamo(idReclamo, idestReclamo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_MODIFICAR_ESTADO_RECLAMO',[idReclamo, idestReclamo,salida])
    return salida.getvalue()

def asignar_repartidor(id, idestpedido,rutrepartidor):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_MODIFICAR_ASIGNAR_REPARTIDOR',[id, idestpedido,rutrepartidor ,salida])
    return salida.getvalue()

def listado_reclamos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_RECLAMOS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista


