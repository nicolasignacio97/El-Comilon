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

def listaEmpresa(request):
    data = {
        'empresa': listarEmpresa()
    }
    return render(request, 'listaEmpConv.html', data)


def listarEmpresa():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_EMP", [out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def empresaRut(request):
    if request.method == 'POST':

        rut = request.POST.get('empresaRut')

        data = {
        'empresa': listarEmpresaRut(rut)
        }
    return render(request, 'listaEmpConv.html', data)


def listarEmpresaRut(rut):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_EMPRESA_RUT", [rut, out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def eliminarEmpresa(request):
    if request.method == 'POST':
        rut = request.POST.get('btnEliminar')
    
    eliminar(rut)

    return listaEmpresa(request)

def eliminar(rut):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()

    cursor.callproc("SP_ELIMINAR_EMPRESA", [rut])

    return 0

def actualizarEmpresa(request):

    if request.method == 'POST':

        rut = request.POST.get('btnActualizar')

        data = {
        'empresa': listarEmpresaRut(rut)
        }

 
    return render(request, 'actEmpConv.html', data)


def actEmpresa(request):
    if request.method =='POST':
        rutEmpresa = request.POST.get('rutEmpresa')
        nombre = request.POST.get('nombreEmpresa')
        razonSocial = request.POST.get('razonSocial')

        actualizar(rutEmpresa, nombre, razonSocial)

    return listaEmpresa(request)

def actualizar(rutEmpresa, nombre, razonSocial):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    cursor.callproc("SP_ACT_EMPRESA", [rutEmpresa, nombre, razonSocial])

    return 0