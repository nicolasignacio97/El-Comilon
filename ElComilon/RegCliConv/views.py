from django.shortcuts import get_object_or_404, render, redirect
from django.db import connection
from core.models import Cliente, EmpresaConvenio
import cx_Oracle

# Create your views here.
#AGREGAR CLIENTES CONVENIO
def RegistroCliConvenio(request):
    data = {

    }
    if request.method == 'POST':
        rutcliente = request.POST.get('rutCliConv')
        nomUsuario = request.POST.get('nomUsuarioConv')
        nombres = request.POST.get('nomCliConv')
        apellidos = request.POST.get('apeCliConv')
        direccion = request.POST.get('direcCliConv')
        contrasena = request.POST.get('passCliConv')
        telefono = request.POST.get('telCliConv')
        correo = request.POST.get('mailCliConv')
        saldocli = request.POST.get('saldoCli')
        idtipoCliente = 1
        rutempcli = request.POST.get('rutEmpConv')
        salida = agregar_cliente_convenio(rutcliente, nomUsuario,nombres, apellidos, direccion, contrasena, telefono, correo,saldocli,idtipoCliente,rutempcli)
        if salida == 1:
            data['mensaje'] = 'CLIENTE CONVENIO AGREGADO CORRECTAMENTE'
        else:
            data['mensaje'] = 'UPS, NO SE HA PODIDO AGREGAR EL CLIENTE CONVENIO'

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
        nomUsuario = request.POST.get('nomUsuarioConv')
        nombres = request.POST.get('nomCliConv')
        apellidos = request.POST.get('apeCliConv')
        direccion = request.POST.get('direcCliConv')
        contrasena = request.POST.get('passCliConv')
        telefono = request.POST.get('telCliConv')
        correo = request.POST.get('mailCliConv')
        saldocli = request.POST.get('saldoCli')
        rutempcli = request.POST.get('rutEmpConv')
        salida = modificar_cliente_convenio(rutclienteConv, nomUsuario,nombres, apellidos, direccion, contrasena, telefono, correo,saldocli,rutempcli)
        if salida == 1:
            return redirect(to="/administracion/listarCliConv")
            # dataMod['mensaje'] = 'CLIENTE CONVENIO MODIFICADO CORRECTAMENTE'
        else:
            dataMod['mensaje'] = 'UPS, NO SE HA PODIDO MODIFICAR EL CLIENTE CONVENIO'
    return render(request,'modCliConv.html',dataMod)



## FUNCIONES DE CLIENTES CONVENIO

#FUNCIÓN AGREGAR CLIENTE CONVENIO
def agregar_cliente_convenio(rutcliente, nomUsuario,nombres, apellidos, direccion, contrasena,telefono,correo,saldocli,idtipoCliente,rutempcli):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_CLIENTE_CONVENIO',[rutcliente, nomUsuario , nombres, apellidos, direccion, contrasena,telefono,correo, saldocli,idtipoCliente,rutempcli,salida])
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




#ELIMINAR CLIENTE CONVENIO
def eliminarCliConv(request, id):
    cliente = get_object_or_404(Cliente,rutcliente=id)
    cliente.delete()
    return redirect(to="/administracion/listarCliConv")
