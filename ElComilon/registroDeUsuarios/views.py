from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from core.models import Cliente
from .forms import FormularioUsuario
from django.contrib import messages
from django.db import connection
import cx_Oracle
from itertools import cycle

def digito_verificador(rut):
    reversed_digits = map(int, reversed(str(rut)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(reversed_digits, factors))
    return (-s) % 11

# Create your views here.

def registroUsuario(request):

    data = {
        'form': FormularioUsuario(),
    }  
    if request.method == 'POST':
            rutcliente = request.POST.get('rut')
            idtipoCliente = 2
            forumulario = FormularioUsuario(data=request.POST)
            if Cliente.objects.filter(rutcliente=rutcliente).exists():
                mensaje = 'Ya existe un usuario con este RUT.'
            else:
                mensaje=''
                if forumulario.is_valid():
                    forumulario.save()
                    user= authenticate(username=forumulario.cleaned_data["username"], password= forumulario.cleaned_data["password1"])
                    agregar_cliente(rutcliente, idtipoCliente)
                    login(request,user)
                    messages.success(request, "Usuario Creado")
                    return redirect(to="home")
            data = {'form': forumulario, 'rut': rutcliente,'mensaje':mensaje}

    return render(request, 'registration/registro.html',data )


def agregar_cliente(rutcliente, idtipocliente):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_CLIENTE',[rutcliente, idtipocliente, salida])
    return salida.getvalue()