from django import forms
from .models import Repartidor, Vehiculo
from django.contrib.auth.forms import UserCreationForm

class formrepartidor(forms.ModelForm):
    class Meta:
        model = Repartidor
        fields = ["RUTREPARTIDOR", "NOMBRES" , "APELLIDOS", "FECHACONTRATO" , "USUARIO", "CONTRASENA", "RUTRESTAURANTE"]

class formvehiculo(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ["PATENTEVEHICULO", "MODELO" , "ANIO", "COLOR" , "RUTREPARTIDOR", "IDTIPOVEHICULO"]