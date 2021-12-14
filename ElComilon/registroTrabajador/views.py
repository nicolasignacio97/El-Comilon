from django.shortcuts import get_object_or_404, redirect, render
from django.db import connection, reset_queries
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User,Group
from django.http.response import JsonResponse
from core.models import Trabajador
from registroDeUsuarios.forms import FormularioUsuario
from django.contrib import messages
import cx_Oracle

# Create your views here.

data = {}
@permission_required('core')
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
       
        rutRestaurante = '99.365.349-8' #CAMBIAR ESTO SEGUN SU BASE DE DATOS

        idCargo = request.POST.get('cargo')
        forumulario = FormularioUsuario(data=request.POST)
        if forumulario.is_valid():
            user = forumulario.save()
            groupAdministrador = Group.objects.get(name='Administrador')
            groupRecepcionista = Group.objects.get(name='Recepcionista')
            if idCargo == '1':
                user.groups.add(groupAdministrador)
            if idCargo == '2':
                user.groups.add(groupRecepcionista)
            REGISTRAR_TRABAJADOR(rutTrabajador, nombres, apellidos, fechaContrato, rutRestaurante, idCargo) 
            messages.success(request, 'Trabajador Registrado con exito')
            return render(request, 'registroTrabajador.html', data)
        data = {'form':forumulario,'campos':[rutTrabajador,nombres,apellidos,fechaContrato,rutRestaurante,idCargo],'cargo': listar()}
     
    return render(request, 'registroTrabajador.html', data)

@permission_required('core')
def clean_rut_trabajador(request):
    ruttrabajador = request.POST.get('rut')
    if Trabajador.objects.filter(ruttrabajador=ruttrabajador).exists():
        return JsonResponse({'valid': 0})
    return JsonResponse({'valid': 1 })

@permission_required('core')   
def listar():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_CARGO", [out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

@permission_required('core')
def REGISTRAR_TRABAJADOR(RUTTRABAJADOR, NOMBRES, APELLIDOS, FECHACONTRATO, RUTRESTAURANTE, IDCARGO):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salidaPrve = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("REGISTRAR_TRABAJADOR", [RUTTRABAJADOR, NOMBRES, APELLIDOS,FECHACONTRATO, RUTRESTAURANTE, IDCARGO, salidaPrve])
    return salidaPrve.getvalue()

@permission_required('core')
def listaTrabajador(request):
    global data
    data = {
        'trabajadores': listarTrabajador()
    }
    return render(request, 'listarTrabajador.html', data)

@permission_required('core')
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
    global data
    if request.method == 'POST':

        rut = request.POST.get('trabajadorRut')

        data = {
        'trabajadores': listarTrabajadorRut(rut)
        }
    return render(request, 'listarTrabajador.html', data)

@permission_required('core')
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
def actualizarTrabajador(request,id):

    trabajador = get_object_or_404(Trabajador,ruttrabajador = id)

    data = {
        'trabajador':trabajador,
        'cargo': listar()
    }
    if request.method =='POST':
        rutTrabajador = request.POST.get('rutTrabajador')
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        idCargo = request.POST.get('cargo')

        actualizar(rutTrabajador, nombres, apellidos, idCargo)
        messages.success(request, nombres + " Actualizado correctamente")

        return redirect(to='listaTrabajador')
    return render(request, 'actualizarTrabajador.html', data)
    
@permission_required('core')
def actualizar(rutTrabajador, nombres, apellidos, idCargo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    cursor.callproc("SP_ACT_TRABAJADOR", [rutTrabajador, nombres, apellidos, idCargo])

    return 0



@permission_required('core')
def eliminarTrabajador(request,rut):
    trabajadores = Trabajador.objects.get(ruttrabajador = rut)
    trabajadores.delete()
    messages.success(request, 'Eliminado con exito')
    return listaTrabajador(request)

@permission_required('core')
def eliminar(rut):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    cursor.callproc("SP_ELIMINAR_TRABAJADOR", [rut])
    return 0