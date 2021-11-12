from .forms import EditarUsuario
from django.shortcuts import get_object_or_404, redirect, render
from core.models import Cliente ,Pedido
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required 

from .forms import EditarUsuario
 #Create your views here.
def PerfilUsuario(request,id):
    usuario = get_object_or_404(Cliente,idcuenta = id)
    pedido = Pedido.objects.filter(rutcliente = usuario.rutcliente).order_by('-fechapedido')
    data = {
            'usuario' : usuario,
            'pedidos' :pedido,
        }
    return render(request,'historialPedidos.html',data)

def perfilMenu(request,id):
    usuario = get_object_or_404(User,id = id)
    form = EditarUsuario(instance = usuario)
    data = {
            'usuario' : usuario,
            'form': form
        }
    if request.method == 'POST':
        form = EditarUsuario(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request,'perfilMenu.html',data)


@login_required()
def CambiarContra (request):
    form = PasswordChangeForm(user=request.user)
    forumulario={'form':form}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'CambioContrasena.html',forumulario)
