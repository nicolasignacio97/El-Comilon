from django.shortcuts import get_object_or_404, render
from core.models import Usuario ,Pedido

# Create your views here.
def PerfilUsuario(request,id):
    usuario = get_object_or_404(Usuario,rut = id)
    pedido = Pedido.objects.filter(rutcliente = id).order_by('-fechapedido')
    data = {
        'usuario' : usuario,
        'pedidos' :pedido,
    }
    return render(request,'historialPedidos.html',data)
    

