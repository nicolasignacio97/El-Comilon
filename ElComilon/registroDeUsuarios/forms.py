from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields


class FormularioUsuario (UserCreationForm):


    class Meta: 
        model = User
        # email = forms.EmailField(label=("Correo electrónico"),widget=forms.EmailInput(
        #  attrs={"minlength": "2","pattern": "[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*@[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*[.][a-zA-Z]{1,5}"}))
        fields =['email','username', 'password1','password2']

