from django.shortcuts import render
from django.db import connection
import cx_Oracle

# Create your views here.
def registroEmpresa(request):
    if request.method == 'POST':
        rutEmpresa = request.POST.get('rutEmpresa')
        nombre = request.POST.get('nombreEmpresa')
        razonSocial = request.POST.get('razonSocial')
        salida = registrarEmpresa(rutEmpresa, nombre, razonSocial)

    return render(request,'regEmpConv.html')

def registrarEmpresa(rutEmpresa, nombre, razonSocial):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)

    cursor.callproc('SP_INSERT_EMP_CONV',[rutEmpresa, nombre, razonSocial, salida])

    return salida.getvalue()
