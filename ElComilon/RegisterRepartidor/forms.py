from typing import Pattern
from django import forms
from django.db.models import fields
from core.models import *

class Repartidorform(forms.ModelForm):
    class Meta:
        model = Repartidor
        fields = ('nombres', 'apellidos', 'fechacontrato')
class vehiculoform(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ('patentevehiculo', 'modelo', 'anio' , 'color')

class registerRepartidor(forms.Form):
    rutrepartidor = forms.CharField(
        required=True,min_length=4,max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control w-50',
            'id':'rutrepartidor'
        })
    )
    def clean_rutrepartidor(self):
        rutrepartidor = self.cleaned_data.get('rutrepartidor')
        if Repartidor.objects.filter(rutrepartidor = rutrepartidor).exists():
            raise ('ERRPR')
        return rutrepartidor