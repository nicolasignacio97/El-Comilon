from django import forms
from django.db.models import fields
from core.models import *

class Repartidorform(forms.ModelForm):
    class Meta:
        model = Repartidor
        fields = ('__all__')
class vehiculoform(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ('__all__')