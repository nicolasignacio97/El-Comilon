from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from .forms import EditarUsuario, EditarRepresentante
from django.contrib.auth.models import User
from core.models import Representante
# Create your views here.
def menuProveedor(request,id):
    usuario = get_object_or_404(User, id=id)
    representante = get_object_or_404(Representante, idcuenta=id)

   
    formCuenta = EditarUsuario(instance=usuario)
    formPersonal = EditarRepresentante(instance=representante)
   
    data = {
        'usuario': usuario,
        'formCuenta': formCuenta,
        'form': formPersonal,
    }
    
    if request.method == 'POST':
        formCuenta = EditarUsuario(request.POST, instance=request.user)
        formPersonal = EditarRepresentante(request.POST, instance=representante)

        if formCuenta.is_valid():
            
            if formPersonal.is_valid():
                formCuenta.save()
                formPersonal.save()
                messages.success(request, " Modificado correctamente")
                usuario = get_object_or_404(User, id=id)
                representante = get_object_or_404(Representante, idcuenta=id)
                
                formCuenta = EditarUsuario(instance=usuario)
                formPersonal = EditarRepresentante(instance=representante)
                data2 = {
                    'usuario': usuario,
                    'formCuenta': formCuenta,
                    'form': formPersonal
                }
                return render(request, 'menuProveedor.html', data2)
    return render (request,'menuProveedor.html',data)

    

def subirPlatilloProveedor(request):
    
    return render (request,'subirPlatilloProveedor.html')

    
def listarPlatilloProveedor(request):
    
    return render (request,'listarPlatillosProveedor.html')