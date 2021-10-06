
from django.http import request
from django.shortcuts import render
from django.db import connection
import cx_Oracle

# Create your views here.
def register (request):
    data = {

    }
    # agregar_cliente('18.127.345-5','nomU','b','c','la estrofa 2050','joaq',65287134, 'hola@hola.cl',2)

    if request.method == 'POST':
        rutcliente = request.POST.get('rutCliente')
        nomUsuario = request.POST.get('nomUsuario')
        nombres = request.POST.get('nombresCli')
        apellidos = request.POST.get('apellidosCli')
        direccion = request.POST.get('direccionCli')
        contrasena = request.POST.get('passUser')
        telefono = request.POST.get('numTelefono')
        correo = request.POST.get('mailUsuario')
        idtipoCliente = 2
        salida = agregar_cliente(rutcliente, nomUsuario,nombres, apellidos, direccion, contrasena, telefono, correo, idtipoCliente)
        if salida == 1:
            data['mensaje'] = 'AGREGADO CORRECTAMENTE'
        else:
            data['mensaje'] = 'UPS, NO SE HA PODIDO AGREGAR'

    return render(request,'registerUser.html', data)



def agregar_cliente(rutcliente, nombreusuario,nombres, apellidos, direccion, contrasena,telefono,correo, idtipocliente):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_CLIENTE',[rutcliente, nombreusuario , nombres, apellidos, direccion, contrasena,telefono,correo, idtipocliente, salida])
    return salida.getvalue()