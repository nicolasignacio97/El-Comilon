from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from core.models import Trabajador,Vehiculo


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

class EditarRecepcionista(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ('nombres','apellidos')
