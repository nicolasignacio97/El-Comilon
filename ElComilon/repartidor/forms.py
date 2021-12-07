from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms.widgets import TextInput
from core.models import Repartidor,Vehiculo


class EditarUsuario (UserChangeForm):
    password = None
    class Meta:
        model=User
        fields=('email','username')

class EditarRepartidor(forms.ModelForm):
    class Meta:
        model = Repartidor
        fields = ('nombres','apellidos')

class EditarVehiculo(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ('patentevehiculo','modelo','anio')
        