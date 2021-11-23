from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.db import connection
from django.contrib import messages
from core.models import Cliente
from django.contrib.auth.models import User
import cx_Oracle
from registroDeUsuarios.forms import FormularioUsuario


# Create your views here.
#AGREGAR CLIENTES CONVENIO
def RegistroCliConvenio(request):
    data = {
        'form': FormularioUsuario(),
        'Seleccion':listar_EmpConvenio()
    }
    if request.method == 'POST':
        rutcliente = request.POST.get('rutCliConv')
        nombres = request.POST.get('nomCliConv')
        apellidos = request.POST.get('apeCliConv')
        direccion = request.POST.get('direcCliConv')
        saldocli = request.POST.get('saldoCli')
        idtipoCliente = 1
        rutempcli = request.POST.get('rutEmpConv')
        forumulario = FormularioUsuario(data=request.POST)
        if forumulario.is_valid():
            forumulario.save()
            data['form'] = forumulario
            agregar_cliente_convenio(rutcliente,nombres, apellidos, direccion,idtipoCliente,rutempcli,saldocli)    
            messages.success(request, "Usuario Creado")
            return render(request,'regCliConv.html', data)
    return render(request,'regCliConv.html', data)
#ValrutCliente
def cleanRutcliente(request):
    rutcliente = request.POST.get('rut')
    print(rutcliente)
    if Cliente.objects.filter(rutcliente=rutcliente).exists():
        print("Repartidor existente")
        return JsonResponse({'valid': 0})
    return JsonResponse({'valid': 1 })


#ELIMINAR CLIENTE CONVENIO
def eliminarCliConv(request,rutcliente, id):
    u = User.objects.get(pk=id)
    u.delete()
    clientes = Cliente.objects.all()
    cliente = Cliente.objects.get(rutcliente=rutcliente)
    cliente.delete()
    messages.success(request, messages.SUCCESS , 'Eliminado con exito')
    contexto = {
         'cliente':clientes
    }
    return listarCliConv(request)
    # return redirect(to="/administracion/listarCliConv")

#LISTAR CLIENTES CONVENIO
def listarCliConv(request):
    # print(listar_clientes_conv())
    dataClientes = {
        'clientesConv':listar_clientes_conv()
    }
    return render(request,'listarCliConv.html',dataClientes)

#MODIFICAR CLIENTE CONVENIO
def modificarCliConv(request,id):
    cliente = get_object_or_404(Cliente,rutcliente=id)
    dataMod = {
       'selection' : cliente
    }

    if request.method == 'POST':

        rutclienteConv = request.POST.get('rutCliConv')
        nombres = request.POST.get('nomCliConv')
        apellidos = request.POST.get('apeCliConv')
        direccion = request.POST.get('direcCliConv')
        saldocli = request.POST.get('saldoCli')
        rutempcli = request.POST.get('rutEmpConv')
        idtipo = 1

        modificar_cliente_convenio(rutclienteConv,nombres, apellidos, direccion,saldocli,idtipo,rutempcli)
        messages.success(request,'Modificado con exito')
        return redirect(to="listarCliConv")

    return render(request,'modCliConv.html',dataMod)



## FUNCIONES DE CLIENTES CONVENIO

#FUNCIÓN AGREGAR CLIENTE CONVENIO
def agregar_cliente_convenio(rutcliente,nombres, apellidos, direccion,idtipoCliente,rutempcli,saldocli):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_CLIENTE_CONVENIO',[rutcliente, nombres, apellidos, direccion, idtipoCliente,rutempcli,saldocli,salida])
    return salida.getvalue()



#FUNCIÓN MODIFICAR CLIENTE CONVENIO
def modificar_cliente_convenio(rutcliente,nombres, apellidos, direccion,saldocli,idtipocliente,rutempcli):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_MODIFICAR_CLIENTE_CONVENIO',[rutcliente, nombres, apellidos, direccion, saldocli,idtipocliente,rutempcli,salida])
    return salida.getvalue()

#FUNCION LISTAR CLIENTE
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



