from django.core.paginator import Paginator
from django.http.response import Http404
from django.db import connection
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
import cx_Oracle

from actualizarPlatillo.views import listado_platillos,listado_fotos, ModificarPlatilloSinFoto, modificarPlatillo

from .forms import EditarUsuario, EditarRepresentante
from django.contrib.auth.models import User
from core.models import Representante, Restaurante,Platillo, DetallePedido
from RegisterPlatillo.views import registrarPlatillo
# Create your views here.


def menuProveedor(request, id):
    usuario = get_object_or_404(User, id=id)
    representante = get_object_or_404(Representante, idcuenta=id)
    representante = get_object_or_404 (Representante,idcuenta = request.user.id)
    restaurante = get_object_or_404(Restaurante,rutrepresentante = representante.rutrepresentante)
    formCuenta = EditarUsuario(instance=usuario)
    formPersonal = EditarRepresentante(instance=representante)
    data = {
        'usuario': usuario,
        'formCuenta': formCuenta,
        'form': formPersonal,
        'TotalPedidos':len(listado_platillos_proveedor(restaurante.rutrestaurante))
    }

    if request.method == 'POST':
        formCuenta = EditarUsuario(request.POST, instance=request.user)
        formPersonal = EditarRepresentante(
            request.POST, instance=representante)

        if formCuenta.is_valid():

            if formPersonal.is_valid():
                formCuenta.save()
                formPersonal.save()
                messages.success(request, " Modificado correctamente")
                usuario = get_object_or_404(User, id=id)
                representante = get_object_or_404(Representante, idcuenta=id)

                formCuenta = EditarUsuario(instance=usuario)
                formPersonal = EditarRepresentante(instance=representante)
                data2 = {
                    'usuario': usuario,
                    'formCuenta': formCuenta,
                    'form': formPersonal
                }
                return render(request, 'menuProveedor.html', data2)
    return render(request, 'menuProveedor.html', data)


def subirPlatilloProveedor(request):
    representante = get_object_or_404 (Representante,idcuenta = request.user.id)
    restaurante = get_object_or_404(Restaurante,rutrepresentante = representante.rutrepresentante)
    data = {
        'TotalPedidos':len(listado_platillos_proveedor(restaurante.rutrestaurante))
    }

    if request.method == 'POST':
        nombrePlatillo = request.POST.get('Nombre').upper()
        ingredientes = request.POST.get('Ingredientes').upper()
        valor = request.POST.get('Valor')
        foto = request.FILES['foto'].read()
        rutRestaurante = restaurante.rutrestaurante
        check1 = request.POST.get('Disponible')
        if check1:
            disponible = 1
        else:
            disponible = 0
        registrarPlatillo(nombrePlatillo, ingredientes, valor, foto, rutRestaurante, disponible)
        messages.success(request, "Se ha creado correctamente el platillo ")
    return render (request,'subirPlatilloProveedor.html',data)

    
def listarPlatilloProveedor(request):
    global data
    representante = get_object_or_404 (Representante,idcuenta = request.user.id)
    restaurante = get_object_or_404(Restaurante,rutrepresentante = representante.rutrepresentante)

    listaPlatillos = Platillo.objects.filter(rutrestaurante = restaurante.rutrestaurante)
    
    page = request.GET.get('page',1)
    Lista = listaPlatillos
    try:
        paginator = Paginator(Lista, 10)
        Lista = paginator.page(page)
    except :
        raise Http404

    data = {
        'entity': Lista,
        'paginator' : paginator,
        'restaurante' : restaurante,
        'TotalPedidos':len(listado_platillos_proveedor(restaurante.rutrestaurante))
    }

    return render (request,'listarPlatillosProveedor.html',data)


def EliminarPlatilloProveedor(request, id):
    platillo = get_object_or_404(Platillo, idplatillo=id)
    platillo.delete()
    messages.success(request, "Se ha eliminado correctamente el platillo "+ platillo.nombre)
    return redirect(to="/listarPlatilloProveedor")


def ModificarPlatilloProveedor(request, id):
    platillo = get_object_or_404(Platillo, idplatillo=id)
    representante = get_object_or_404 (Representante,idcuenta = request.user.id)
    restaurante = get_object_or_404(Restaurante,rutrepresentante = representante.rutrepresentante)
    dataMod = {
        'platillo':listado_platillos(id),
        'foto':listado_fotos(id),
        'TotalPedidos':len(listado_platillos_proveedor(restaurante.rutrestaurante))
    }
    if request.method == 'POST':
        nombrePlatillo = request.POST.get('Nombre').upper()
        ingredientes = request.POST.get('Ingredientes').upper()
        valor = request.POST.get('Valor')
        checkDisponible = request.POST.get('Disponible')
        checkStock = request.POST.get('Stock')
        if checkDisponible:
            disponible = 1
        else:
            disponible = 0

        if checkStock:
            stock = 1
        else:
            stock = 0
        if 'foto' in request.POST:
         foto = False
         ModificarPlatilloSinFoto(id,nombrePlatillo, ingredientes, valor,disponible, stock)
        else:
         foto = True
         foto = request.FILES['foto'].read()
         modificarPlatillo(id,nombrePlatillo, ingredientes, valor, foto,disponible, stock)
        messages.success(request, "Se ha modificado correctamente el platillo "+ platillo.nombre)
        return redirect(to="/listarPlatilloProveedor")
    return render (request,'modificarPlatilloProveedor.html',dataMod)

def PlatillosPendientes(request):
    representante = get_object_or_404 (Representante,idcuenta = request.user.id)
    restaurante = get_object_or_404(Restaurante,rutrepresentante = representante.rutrepresentante)
    data = {
        'platillos':listado_platillos_proveedor(restaurante.rutrestaurante),
        'TotalPedidos':len(listado_platillos_proveedor(restaurante.rutrestaurante))
    }
    return render (request,'platillosPendientes.html',data)


def cambiarAPreparacion(request ,id):
    cambiar_estado_platillo(id,2)
    return redirect(to='PlatillosPendientes')

def cambiarAPendiente(request ,id):
    cambiar_estado_platillo(id,1)
    return redirect(to='PlatillosPendientes')

def cambiarAListo(request ,id):
    cambiar_estado_platillo(id,3)
    return redirect(to='PlatillosPendientes')


def listado_platillos_proveedor(rut):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PLATILLOS_PROVEEDOR", [rut,out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista




def cambiar_estado_platillo(iddetalle, idEstado):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_MODIFICAR_ESTADO_PLATILLO',[iddetalle, idEstado,salida])
    return salida.getvalue()