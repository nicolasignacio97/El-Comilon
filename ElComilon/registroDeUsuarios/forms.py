from django import  forms
from core.models import  UsuarioGeneral

class  FormularioUsuario (forms.ModelForm):

    password1 = forms.CharField(label=("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Password (again)"), widget=forms.PasswordInput)

    class Meta:
        model = UsuarioGeneral
        fields = 'email','username','nombres','apellidos'
        widget={

        }

    # def clean_password2(sef):
    #     password1 = sef.cleaned_data.get('password')
    #     password2 = sef.cleaned_data.get('password2')
    #     if password1 != password2:
    #         raise forms.ValidationError('contraseña no coinciden')
    #     return password2
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return password2
        
    def save(self,commit=True):
        usuario = super().save(commit=True)
        usuario.set_password(self.cleaned_data['password2'])
        if commit:
            usuario.save()
        return usuario


