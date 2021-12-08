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

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ya existe un usuario con este nombre.")
        return username
        
class EditarRepartidor(forms.ModelForm):
    class Meta:
        model = Repartidor
        fields = ('nombres','apellidos')

class EditarVehiculo(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ('patentevehiculo','modelo','anio')
        