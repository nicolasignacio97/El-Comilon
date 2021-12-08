from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from core.models import Trabajador,Vehiculo


class EditarUsuario (UserChangeForm):
    password = None
    class Meta:
        model=User
        fields=('email','username')


class EditarRecepcionista(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ('nombres','apellidos')
