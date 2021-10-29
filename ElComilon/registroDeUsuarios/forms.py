from django import forms
from core.models import Usuario



class FormularioUsuario (forms.ModelForm):
    password1 = forms.CharField(
        label=("Contraseña"), widget=forms.PasswordInput(
            attrs={"class": "form-control"}))
    password2 = forms.CharField(
        label=("Confirmar Contraseña"), widget=forms.PasswordInput(
            attrs={"class": "form-control"}))

    email = forms.EmailField(label=("Correo electrónico"),widget=forms.EmailInput(
        attrs={"pattern": "[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*@[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*[.][a-zA-Z]{1,5}"}))

    username = forms.CharField(
        label=("Nombre de usuario"), widget=forms.TextInput(
            attrs={"minlength": "2"}))

    nombres = forms.CharField(
        label=("Nombres "), widget=forms.TextInput(
            attrs={"minlength": "2"}))

    apellidos = forms.CharField(
        label=("Apellidos"), widget=forms.TextInput(
            attrs={"minlength": "2"}))

    rut = forms.CharField(
        label=("Rut"), widget=forms.TextInput(
            attrs={"class": "input_rut","id":"Rut", "oninput":"checkRut(this)"}))
    class Meta:
        model = Usuario
        fields = ('rut','email', 'username', 'nombres', 'apellidos')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(("Las contraseñas no coinciden"))
        return password2

    def save(self, commit=True):
        usuario = super().save(commit=True)
        usuario.set_password(self.cleaned_data['password2'])
        if commit:
            usuario.save()
        return usuario    
