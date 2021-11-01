from django import forms
from core.models import *

class Repartidorform(forms.ModelForm):
    class Meta:
        model = Repartidor
        fields = ('__all__')