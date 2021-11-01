from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render

def usuarionoautenticado(view_func):
    def wrapper_funk(request, *args, **kwargs):
        if request.user.is_authenticated:
            redirect('perfil')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_funk