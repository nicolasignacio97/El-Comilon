from django import forms
from django.contrib.auth import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.forms import Form

class FormularioUsuario (UserCreationForm):

    class Meta: 
        model = User
        fields =['email','username', 'password1','password2']
        
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ya existe un usuario con este nombre.")
        return username
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con este Correo.")
        return email


        # email = forms.EmailField(label=("Correo electrónico"),widget=forms.EmailInput(
        #  attrs={"minlength": "2","pattern": "[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*@[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*[.][a-zA-Z]{1,5}"}))
