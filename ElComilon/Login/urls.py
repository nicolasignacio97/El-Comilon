from django.urls import path
from Login import views
from PerfilUsuario.views import Usertemplate


app_name = "Login"

urlpatterns = [
    path('', views.login, name='login'),
    path('perfil',Usertemplate)

]