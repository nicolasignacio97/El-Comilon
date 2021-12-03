from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from core.models import Cliente



class EditarCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('nombres', 'apellidos', 'direccion', 'telefono')


class EditarUsuario (UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['email', 'username']
        labels = {
            'email': 'Correo Electrónico',
            'username': 'Nombre de Usuario'
        }


class EditarContrasena(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password','new_password1','new_password2')
    def clean_new_password1(self):
        data = self.cleaned_data['new_password1']
        if len(data) < 8 or len(data) > 64:
          raise forms.ValidationError("La nueva contraseña debe tener un mínimo de 8 caracteres y un máximo de 64 caracteres")
        return data