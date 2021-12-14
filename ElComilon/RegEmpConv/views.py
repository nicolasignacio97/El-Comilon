from django.contrib.auth.decorators import permission_required
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db import connection
from django.contrib import messages
from core.models import EmpresaConvenio
import cx_Oracle

# Create your views here.

data = {}
@permission_required('core')
def registroEmpresa(request):
    data = {
    'restaurante':listar_restaurantes()
    }
    if request.method == 'POST':
        rutEmpresa = request.POST.get('rutEmpresa')
        nombre = request.POST.get('nombreEmpresa')
        razonSocial = request.POST.get('razonSocial')
        fechaconvenio = request.POST.get('fechaconvenio')
        registrarEmpresa(rutEmpresa, nombre, razonSocial,fechaconvenio)
        messages.success(request,'Agregado correctamente')
    return render(request,'regEmpConv.html',data)

def clean_rut_emp_convenio(request):
    rutrempresa = request.POST.get('rut')
    if EmpresaConvenio.objects.filter(rutempresaconvenio=rutrempresa).exists():
        return JsonResponse({'valid': 0})
    return JsonResponse({'valid': 1 })

@permission_required('core')
def listaEmpresa(request):
    global data
    data = {
        'empresa': listarEmpresa()
    }
    return render(request, 'listaEmpConv.html', data)


@permission_required('core')
def empresaRut(request):
    global data
    if request.method == 'POST':
        rut = request.POST.get('empresaRut')

        data = {
        'empresa': listarEmpresaRut(rut)
        }
    return render(request, 'listaEmpConv.html', data)


@permission_required('core')
def eliminarEmpresa(request):
    if request.method == 'POST':
        rut = request.POST.get('btnEliminar')
    
        eliminar(rut)
        messages.success(request,'Empresa Eliminada')
    return listaEmpresa(request)

@permission_required('core')
def actualizarEmpresa(request):

    if request.method == 'POST':

        rut = request.POST.get('btnActualizar')

        data = {
        'empresa': listarEmpresaRut(rut)
        }
    
    return render(request, 'actEmpConv.html', data)
@permission_required('core')
def actEmpresa(request):
    if request.method =='POST':
        rutEmpresa = request.POST.get('rutEmpresa')
        nombre = request.POST.get('nombreEmpresa')
        razonSocial = request.POST.get('razonSocial')
        fechacontrato = request.POST.get('fechacontrato')
        messages.success(request,'Actualizado')
        actualizar(rutEmpresa, nombre, razonSocial,fechacontrato)

    return listaEmpresa(request)

@permission_required('core')
def eliminar(rut):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()

    cursor.callproc("SP_ELIMINAR_EMPRESA", [rut])

    return 0

@permission_required('core')
def registrarEmpresa(rutEmpresa, nombre, razonSocial,FECHACONVENIO):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)

    cursor.callproc('sp_insert_emp_convenio',[rutEmpresa, nombre, razonSocial,FECHACONVENIO, salida])

    return salida.getvalue()

@permission_required('core')
def actualizar(rutEmpresa, nombre, razonSocial,FECHACONVENIO):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    cursor.callproc("SP_ACT_EMPRESA", [rutEmpresa, nombre, razonSocial,FECHACONVENIO])

@permission_required('core')
def listar_restaurantes():
    django_cursor = connection.cursor() 
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    cursor.callproc("SP_LISTAR_RESTAURANTE", [out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

@permission_required('core')
def listarEmpresaRut(rut):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_EMPRESA_RUT", [rut, out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

@permission_required('core')
def listarEmpresa():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_EMP", [out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

@permission_required('core')
def EliminarEmpresa(request, id):
    empresa = get_object_or_404(EmpresaConvenio, rutempresaconvenio=id)
    empresa.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to="listaEmpresa")