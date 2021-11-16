from django import forms
from django.contrib.auth import models
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import fields
from core.models import Cliente

class EditarCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('nombres','apellidos','direccion','telefono')
        
class EditarUsuario (UserChangeForm):
    password = None
    class Meta:
        model=User
        fields=('email','username')
        