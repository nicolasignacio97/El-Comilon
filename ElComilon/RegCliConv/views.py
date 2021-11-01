from django.shortcuts import get_object_or_404, render, redirect
from django.db import connection
from core.models import Cliente
import cx_Oracle
from registroDeUsuarios.forms import FormularioUsuario
from django.contrib import messages

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
            agregar_cliente_convenio(rutcliente,nombres, apellidos, direccion,idtipoCliente,rutempcli,saldocli)    
            messages.success(request, "Usuario Creado")
            data['form'] = forumulario
            redirect(to="ClienteConvenio")
    return render(request,'regCliConv.html', data)

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

        modificar_cliente_convenio(rutclienteConv,nombres, apellidos, direccion,saldocli,rutempcli)
     
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
def modificar_cliente_convenio(rutcliente, nomUsuario,nombres, apellidos, direccion, contrasena,telefono,correo,saldocli,rutempcli):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_MODIFICAR_CLIENTE_CONVENIO',[rutcliente, nomUsuario , nombres, apellidos, direccion, contrasena,telefono,correo, saldocli,rutempcli,salida])
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


#ELIMINAR CLIENTE CONVENIO
def eliminarCliConv(request, id):
    cliente = get_object_or_404(Cliente,rutcliente=id)
    cliente.delete()
    return redirect(to="/administracion/listarCliConv")
