from django.shortcuts import render
from .forms import formlog
from django.http import HttpResponseRedirect
from Login.models import Cliente
from django.contrib.auth import authenticate, login , logout
from .decoratators import usuarionoautenticado

# Create your views here.
# def login (request):
#     form = formlog()
#     if request.method == 'POST':
#         formulario = formLog(request.POST)
#         nombreusuario = request
#         if formulario.is_valid():
#             nombreusuario = request.POST['nombreusuario']
#             contrasena = request.POST['contrasena']

#             verificacion = Cliente.objects.filter(nombreusuario=nombreusuario, contrasena=contrasena).exists()
#             print(verificacion)
#             return HttpResponseRedirect('/')

#     return render(request,'iniciar_sesion.html',{'formulario':form})

# del login_template(request):
#     template_name : "home/iniciar_sesion.html"
#     context = {}
#     context []
#     if request.POST:
#         nombreusuario = request.POST['nombreusuario']
#         contrasena = request.POST['contrasena']

from django.shortcuts import render
from .forms import formlog
from django.http import HttpResponseRedirect
from Login.models import Cliente

# Create your views here.
def loginauth (request):
    if request.method == 'POST':
        nombreusuario = request.POST.get('nombreusuario')
        contrasena = request.POST.get('contrasena')
        print('hola if')
        try:
            print('hola')
            cliente = Cliente.objects.get(nombreusuario=nombreusuario,contrasena=contrasena)
            return HttpResponseRedirect('perfil')
        except:
            print("No existe el usuario") 
            return render(request,'iniciar_sesion.html', {'mensaje':'Usuario ingresado no es valido'}) 
    return render(request,'iniciar_sesion.html')