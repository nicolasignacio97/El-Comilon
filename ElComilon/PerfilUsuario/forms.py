from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import Field

class EditarUsuario (UserChangeForm):
    password = None
    class Meta:
        model=User
        fields=('email','username')
        
       

