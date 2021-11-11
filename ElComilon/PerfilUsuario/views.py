from django.shortcuts import get_object_or_404, render
from core.models import Cliente ,Pedido

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
    usuario = get_object_or_404(Cliente,idcuenta = id)
    data = {
            'usuario' : usuario,
        }
    return render(request,'perfilMenu.html',data)
    
