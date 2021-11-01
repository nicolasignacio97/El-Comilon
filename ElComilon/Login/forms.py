from django import forms
from .models import Cliente

class formlog(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombreusuario", "contrasena"]