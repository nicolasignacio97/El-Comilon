from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import CreateView
# from core.models import Usuario
from .forms import FormularioUsuario
from django.contrib import messages
from django.db import connection
import cx_Oracle

# Create your views here.


def registroUsuario(request):
    data = {
        'form': FormularioUsuario()
    }
    if request.method == 'POST':
            rutcliente = request.POST.get('rutCliente')
            # nombres = request.POST.get('nombresCli')
            # apellidos = request.POST.get('apellidosCli')
            # direccion = request.POST.get('direccionCli')
            idtipoCliente = 2
            forumulario = FormularioUsuario(data=request.POST)
            if forumulario.is_valid():
                forumulario.save()
                user= authenticate(username=forumulario.cleaned_data["username"], password= forumulario.cleaned_data["password1"])
                agregar_cliente(rutcliente, idtipoCliente)
                login(request,user)
                messages.success(request, "Usuario Creado")
                return redirect(to="home")
            data['form'] = forumulario
    return render(request, 'registration/registro.html',data )



def agregar_cliente(rutcliente, idtipocliente):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_CLIENTE',[rutcliente, idtipocliente, salida])
    return salida.getvalue()

# class  RegistrarUsuario(CreateView):
#      model = UsuarioGeneral
#      form_class = FormularioUsuario
#      template_name = 'registration/registro.html'
#      success_url = reverse_lazy('login')