from django.contrib import messages
from django.db.utils import DatabaseError
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .context_processors import total_carrito
from django.db import connection
from django.conf import settings
from django.core.mail import send_mail
import cx_Oracle
from Platillos.carrito import carrito
from core.models import Platillo, Cliente, Restaurante
import base64
import datetime

# Create your views here.

def FinalizarCompra(request):
    # AGREGAR DETALLES PEDIDO
    cliente = get_object_or_404(Cliente, idcuenta=request.user.id)
    hora = datetime.datetime.now().strftime('%H:%M')

    dataCli = {
        'horaactual': hora,
        'cliente': cliente,
    }

    return render(request, 'finalizarCompra.html', dataCli)


def platillos(request):
    data = {
        'platillos': listado_platillos(),
        'restaurantes':listado_restaurantes()
    }
    return render(request, 'platillos.html', data)


def listado_platillos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PLATILLOS_DISPO", [out_cur])

    lista = []
    for fila in out_cur:
        data = {
            'data': fila,
            'imagen': str(base64.b64encode(fila[4].read()), 'utf-8')
        }
        lista.append(data)
    return lista


def agregar_producto(request, id):
    Carrito = carrito(request)
    producto = Platillo.objects.get(idplatillo=id)
    Carrito.agregar(producto)
    return redirect("platillos")

def agregar_producto_menu(request, id):
    Carrito = carrito(request)
    producto = Platillo.objects.get(idplatillo=id)
    Carrito.agregar(producto)
    return redirect("FinalizarCompra")


def agregar_producto_fin(request, id):
    Carrito = carrito(request)
    producto = Platillo.objects.get(idplatillo=id)
    Carrito.agregar(producto)
    return redirect("FinalizarCompra")


def eliminar_producto(request, id):
    Carrito = carrito(request)
    producto = Platillo.objects.get(idplatillo=id)
    Carrito.eliminiar(producto)
    return redirect("platillos")


def restar_producto(request, id):
    Carrito = carrito(request)
    producto = Platillo.objects.get(idplatillo=id)
    Carrito.restar(producto)
    return redirect("platillos")


def restar_producto_fin(request, id):
    Carrito = carrito(request)
    producto = Platillo.objects.get(idplatillo=id)
    Carrito.restar(producto)
    return redirect("FinalizarCompra")


def limpiar_carrito(request):
    Carrito = carrito(request)
    Carrito.limpiar()
    return redirect("platillos")


def guardar(request):
    cliente = get_object_or_404(Cliente, idcuenta=request.user.id)
    Carrito = carrito(request)
    saldo = cliente.saldocli
    print('saldo inicial', saldo)
    if request.method == 'POST':
        # ruta
        id = request.user.id
        url = 'estadoPedido/'+str(id)
        # AGREGAR PEDIDO
        total = total_carrito(request)['total_carrito']
        fecha = request.POST.get('Fecha')
        direccion = request.POST.get('Direccion')
        check1 = request.POST.get('Domicilio')
        checkSaldo = request.POST.get('saldo')
        rutcliente = cliente.rutcliente
        idEstPed = 1
        hora = request.POST.get('Hora')
        Carrito = carrito(request)
        carro = Carrito.caja()

        if check1:
            idTipoServ = 1
        else:
            idTipoServ = 2

        if checkSaldo:
            if saldo < total:
                dataCli = {
                    'cliente': cliente,
                    'mensaje':'Saldo Insuficiente',
                    'saldo':saldo
                }   
                return render(request, 'finalizarCompra.html', dataCli)
                
            else:
                saldoActual = saldo - total
                actualizarSaldo(cliente.rutcliente, saldoActual)
                agregar_pedido(total, fecha, direccion, idTipoServ, rutcliente, idEstPed, hora)
            for p in carro:
                agregar_detalle_pedido( p['cantidad'], p['valorunitario'], p['acumulado'], p['idplatillo'], cliente.rutcliente)
            limpiar_carrito(request)
            return redirect(url)
        else:
            carro = Carrito.caja()
            agregar_pedido(total, fecha, direccion, idTipoServ,rutcliente, idEstPed, hora)
            for p in carro:
                print(p['idplatillo'])
                agregar_detalle_pedido(p['cantidad'], p['valorunitario'], p['acumulado'], p['idplatillo'], cliente.rutcliente)
            subjet = "Pedido"
            message = "Hola"
            email_from = settings.EMAIL_HOST_USER
            recipient_list=[request.user.email]
            send_mail(subjet,message,email_from,recipient_list)
            limpiar_carrito(request)
            return redirect(url)


def agregar_pedido(valorTotal, fecha, direccion, idTipoServ, rutCliente, idEstPed, hora):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_AGREGAR_PEDIDO", [
                    valorTotal, fecha, direccion, idTipoServ, rutCliente, idEstPed, hora, salida])
    return salida.getvalue()


def agregar_detalle_pedido(cantidad, valorUnitario, valorTotal, idPlatillo, rutCliente):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_AGREGAR_DETALLE_PEDIDO", [
                    cantidad, valorUnitario, valorTotal, idPlatillo, rutCliente, salida])
    return salida.getvalue()


def actualizarSaldo(rutCliente, saldoNuevo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_ACTUALIZAR_SALDO_COMPRA", [
                    rutCliente, saldoNuevo, salida])
    return salida.getvalue()

def listado_restaurantes():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_RESTAURANTE", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista


def platilloRut(request):
    global data
    if request.method == 'POST':

        rut = request.POST.get('Restaurante')
        print(rut)

        data = {
        'platillos': listarPlatilloRut(rut),
        'restaurantes':listado_restaurantes()
        }
    return render(request, 'platillos.html', data)


def listarPlatilloRut(rut):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PLATILLOS_RUT", [rut, out_cur])

    lista = []
    for fila in out_cur:
        data = {
            'data': fila,
            'imagen': str(base64.b64encode(fila[4].read()), 'utf-8')
        }
        lista.append(data)
    return lista