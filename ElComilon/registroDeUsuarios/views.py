from django.shortcuts import redirect, render
from django.contrib.auth import  authenticate,login
from django.urls import  reverse_lazy
from django.views.generic import  CreateView
from core.models import Usuario
from .forms import FormularioUsuario
from django.contrib import messages

# Create your views here.
def registroUsuario (request):
     data ={
         'form' :FormularioUsuario()
     }
     if  request.method == 'POST':
         forumulario = FormularioUsuario(data = request.POST )
         if forumulario.is_valid():
             forumulario.save()
             messages.success(request,"Usuario Creado")
             return redirect(to="login")
         data['form'] = forumulario
     return render(request, 'registration/registro.html',data )

# class  RegistrarUsuario(CreateView):
#     model = UsuarioGeneral
#     form_class = FormularioUsuario
#     template_name = 'registration/registro.html'
#     success_url = reverse_lazy('login')