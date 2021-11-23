from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.db import connection, reset_queries
from django.contrib.auth.decorators import permission_required
from core.models import Trabajador
from registroDeUsuarios.forms import FormularioUsuario
from django.contrib import messages
from django.contrib.auth.models import User
import cx_Oracle

# Create your views here.
def registroTrabajador(request):
    data = {
        'form': FormularioUsuario(),
        'cargo': listar()
    }
    if request.method == 'POST':
        rutTrabajador = request.POST.get('rutTrabajador')
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        fechaContrato = request.POST.get('fecha')
        rutRestaurante = '77.684.154-9'
        idCargo = request.POST.get('cargo')
        forumulario = FormularioUsuario(data=request.POST)
        # if Trabajador.objects.filter(ruttrabajador = rutTrabajador).exists():
        #     print("Trabajador existente")
        #     messages.error(request, 'Trabajador ya existente')
        # else:
        if forumulario.is_valid():
            forumulario.save()
            data['form'] = forumulario
            REGISTRAR_TRABAJADOR(rutTrabajador, nombres, apellidos, fechaContrato, rutRestaurante, idCargo) 
            messages.success(request, 'Trabajador Registrado con exito')
            return render(request, 'registroTrabajador.html', data)   
    return render(request, 'registroTrabajador.html', data)

def pruebatrabajo(request):
    return render (request, "registroTrabajador.html")
    
def clean_rut_trabajador(request):
    ruttrabajador = request.POST.get('rut')
    print(ruttrabajador)
    if Trabajador.objects.filter(ruttrabajador=ruttrabajador).exists():
        print("Trabajador existente")
        return JsonResponse({'valid': 0})
    return JsonResponse({'valid': 1 })
    
def listar():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_CARGO", [out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def REGISTRAR_TRABAJADOR(RUTTRABAJADOR, NOMBRES, APELLIDOS, FECHACONTRATO, RUTRESTAURANTE, IDCARGO):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salidaPrve = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("REGISTRAR_TRABAJADOR", [RUTTRABAJADOR, NOMBRES, APELLIDOS,FECHACONTRATO, RUTRESTAURANTE, IDCARGO, salidaPrve])
    return salidaPrve.getvalue()


def listaTrabajador(request):
    data = {
        'trabajadores': listarTrabajador()
    }
    return render(request, 'listarTrabajador.html', data)


def listarTrabajador():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_TRABAJADORES", [out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

@permission_required('core')
def trabajadorRut(request):
    if request.method == 'POST':

        rut = request.POST.get('trabajadorRut')

        data = {
        'trabajadores': listarTrabajadorRut(rut)
        }
    return render(request, 'listarTrabajador.html', data)


def listarTrabajadorRut(rut):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_TRABAJADORES_RUT", [rut, out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista
@permission_required('core')
def actualizarTrabajador(request):

    if request.method == 'POST':

        rut = request.POST.get('btnActualizar')

        data = {
        'trabajador': listarTrabajadorRut(rut),
        'cargo': listar()
        }

 
    return render(request, 'actualizarTrabajador.html', data)
    
@permission_required('core')
def actTrabajador(request):
    if request.method =='POST':
        rutTrabajador = request.POST.get('rutTrabajador').upper()
        nombres = request.POST.get('nombres').upper()
        apellidos = request.POST.get('apellidos').upper()
        usuario = request.POST.get('nombreU')
        idCargo = request.POST.get('cargo')

        actualizar(rutTrabajador, nombres, apellidos, usuario, idCargo)

    return listaTrabajador(request)

def actualizar(rutTrabajador, nombres, apellidos, usuario, idCargo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    cursor.callproc("SP_ACT_TRABAJADOR", [rutTrabajador, nombres, apellidos, usuario, idCargo])

    return 0

def eliminarTrabajador(request,ruttrabajador, id):
    u = User.objects.get(pk=id)
    u.delete()
    trabajadores = Trabajador.objects.get(ruttrabajador = ruttrabajador)
    trabajadores.delete()
    messages.success(request, messages.SUCCESS , 'Eliminado con exito')
    contexto = {
         'trabajadores':trabajadores
    }
    return listaTrabajador(request)

# def eliminarTrabajador(request):
#     if request.method == 'POST':
#         rut = request.POST.get('btnEliminar')
    
#     eliminar(rut)

#     return listaTrabajador(request)

def eliminar(rut):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()

    cursor.callproc("SP_ELIMINAR_TRABAJADOR", [rut])

    return 0