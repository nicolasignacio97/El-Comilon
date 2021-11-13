from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


class EditarUsuario (UserChangeForm):
    password = None
    class Meta:
        model=User
        fields=('email','username')
        