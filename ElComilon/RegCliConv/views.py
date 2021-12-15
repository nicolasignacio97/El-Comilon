from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import permission_required
from django.http.response import Http404, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from core.models import Cliente
from django.contrib.auth.models import User
from registroDeUsuarios.forms import FormularioUsuario
from tablib import Dataset
from django.db import connection
import cx_Oracle

# Create your views here.

dataClientes = {}

# AGREGAR CLIENTES CONVENIO

@permission_required('core')
def RegistroCliConvenio(request):
    data = {
        'form': FormularioUsuario(),
        'Seleccion': listar_EmpConvenio()
    }

    if request.method == 'POST':
        rutcliente = request.POST.get('rutCliConv')
        nombres = request.POST.get('nomCliConv')
        apellidos = request.POST.get('apeCliConv')
        direccion = request.POST.get('direcCliConv')
        saldocli = request.POST.get('saldoCli')
        idtipoCliente = 1
        rutempcli = request.POST.get('rutEmpConv')
        formulario = FormularioUsuario(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            agregar_cliente_convenio(rutcliente, nombres, apellidos, direccion, idtipoCliente, rutempcli, saldocli)
            messages.success(request, "Usuario de " + nombres +" creado")
            return render(request, 'regCliConv.html', data)
        data = {
            'form': formulario,
            'campos': [rutcliente, nombres, apellidos, direccion, rutempcli, saldocli, rutempcli],
            'Seleccion': listar_EmpConvenio()
        }

    return render(request, 'regCliConv.html', data)
# ValrutCliente


def cleanRutcliente(request):
    rutcliente = request.POST.get('rut')
    print(rutcliente)
    if Cliente.objects.filter(rutcliente=rutcliente).exists():
        print("Repartidor existente")
        return JsonResponse({'valid': 0})
    return JsonResponse({'valid': 1})


# ELIMINAR CLIENTE CONVENIO
def eliminarCliConv(request, rutcliente):
    cliente = Cliente.objects.get(rutcliente=rutcliente)
    cliente.delete()
    messages.success(request, 'Eliminado con exito')
    return redirect(to="/administracion/listarCliConv")

# LISTAR CLIENTES CONVENIO

@permission_required('core')
def listarCliConv(request):
    global dataClientes
    page = request.GET.get('page',1)
    Lista =  listar_clientes_conv()
    try:
        paginator = Paginator(Lista, 10)
        Lista = paginator.page(page)
    except :
        raise Http404

    dataClientes = {
        'entity': Lista,
        'paginator' : paginator,
    }

    return render(request, 'listarCliConv.html', dataClientes)

# MODIFICAR CLIENTE CONVENIO

@permission_required('core')
def modificarCliConv(request, id):
    cliente = get_object_or_404(Cliente, rutcliente=id)
    dataMod = {
       'selection': cliente
    }

    if request.method == 'POST':

        rutclienteConv = request.POST.get('rutCliConv')
        nombres = request.POST.get('nomCliConv')
        apellidos = request.POST.get('apeCliConv')
        direccion = request.POST.get('direcCliConv')
        saldocli = request.POST.get('saldoCli')
        rutempcli = request.POST.get('rutEmpConv')
        idtipo = 1

        modificar_cliente_convenio(
            rutclienteConv, nombres, apellidos, direccion, saldocli, rutempcli)
        messages.success(request, 'Cliente '+nombres +' '+ apellidos+' modificado con exito')
        return redirect(to="listarCliConv")

    return render(request, 'modCliConv.html', dataMod)


# FUNCIONES DE CLIENTES CONVENIO

# FUNCIÓN AGREGAR CLIENTE CONVENIO
def agregar_cliente_convenio(rutcliente, nombres, apellidos, direccion, idtipoCliente, rutempcli, saldocli):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_CLIENTE_CONVENIO', [
                    rutcliente, nombres, apellidos, direccion, idtipoCliente, rutempcli, saldocli, salida])
    return salida.getvalue()


# FUNCIÓN MODIFICAR CLIENTE CONVENIO
def modificar_cliente_convenio(rutcliente, nombres, apellidos, direccion, saldocli, rutempcli):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_MODIFICAR_CLIENTE_CONVENIO', [
                    rutcliente, nombres, apellidos, direccion, saldocli, rutempcli, salida])
    return salida.getvalue()

# FUNCION LISTAR CLIENTE
def listar_clientes_conv():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_CLIENTES_CONV', [out_cur])

    listaCli = []
    for fila in out_cur:
        listaCli.append(fila)
    return listaCli


def listar_EmpConvenio():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc('LISTAR_EMPCONVENIO', [out_cur])

    ListaConv = []
    for fila in out_cur:
        ListaConv.append(fila)
    return ListaConv


@permission_required('core')
def cliConvRut(request):
    global dataClientes
    
    if request.method == 'POST':

        rut = request.POST.get('cliConvRut')

        dataClientes = {
        'entity': listarCliConvRut(rut)
    }
    return render(request, 'listarCliConv.html', dataClientes)


def listarCliConvRut(rut):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_CLIENTES_CONV_RUT", [rut, out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

@permission_required('core')
def actualizarSaldo(request):
    if request.method == 'POST':
        archivo = request.FILES['arch'];
        datos = leerArchivo(archivo)
        for campos in datos:
            modificar_saldo_cliente(campos[0],campos[1])

    return render(request, 'actualizarSaldo.html')


def leerArchivo(archivo):
    dataset = Dataset()
    nuevoSaldo = archivo
    importar = dataset.load(nuevoSaldo.read(),format='xlsx')

    return importar


def modificar_saldo_cliente(rutempcli,saldocli):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_MODIFICAR_SALDO_CLIENTE', [rutempcli,saldocli,  salida])
    return salida.getvalue()
# 