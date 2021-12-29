from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import permission_required
from django.db import connection
from core.models import Repartidor
from registroDeUsuarios.forms import FormularioUsuario
from .forms import registerRepartidor
from django.contrib import messages
from django.contrib.auth.models import User,Group
import cx_Oracle
from core.models import *


contexto = {}

@permission_required('core')
def Registrorep(request):

    data = {
          'categoria':listar_categoria(),
          'restaurante':listar_restaurantes(),
          'form' :FormularioUsuario()
    }
    if request.method == 'POST':
        #Repartidor
        rutrepartidor = request.POST.get('RutRepartidor')
        nombres = request.POST.get('NombresRepartido')
        apellido = request.POST.get('ApellidosRepartidor')
        fechacontrato = request.POST.get('Fechacontrato')
    
        rutrestaurante = '77.684.154-9'
    
        #Vehiculo
        vehiculorut = request.POST.get('RutRepartidor')
        patente = request.POST.get('Patente')
        modelo = request.POST.get('Modelo')
        ano = request.POST.get('Ano')
        color = request.POST.get('Color') 
        tipovehiculo = request.POST.get('tipovehiculo') 
        forumulario = FormularioUsuario(data=request.POST)
        if forumulario.is_valid():
            user = forumulario.save()
            group = Group.objects.get(name='Repartidor')
            user.groups.add(group)
            agregar_repartidor(rutrepartidor, nombres, apellido, fechacontrato, rutrestaurante)
            agregar_vehiculo(patente,modelo,ano,color,vehiculorut,tipovehiculo)
            messages.success(request, 'Repartidor Registrado con exito')
            return render(request, 'Registrorepartidor.html', data)     
        data = {
            'categoria':listar_categoria(),
            'form' : forumulario,
            'campos':[rutrepartidor,nombres,apellido,fechacontrato,vehiculorut,patente,modelo,ano,color,tipovehiculo]
        }
    return render(request, 'Registrorepartidor.html', data)  

def clean_rut(request):
    rutrepartidor = request.POST.get('rut')
    patente = request.POST.get('patente')
    dic = {}
    print(rutrepartidor)
    if Repartidor.objects.filter(rutrepartidor=rutrepartidor).exists():
        dic['val_rut'] = False
        print("Repartidor existente")
        # return JsonResponse({'valid': 0})
    if Vehiculo.objects.filter(patentevehiculo = patente):
        dic['val_patente'] = False
        print("patente existente")
    return JsonResponse(dic)

#Clean_patente
def clean_patente(request):
    patente = request.POST.get('patente')
    patentenew = request.POST.get('patentenew')
    print(patente)
    print(patentenew)
    dic = {}
    if patente == patentenew:
        dic['val_patenteiguales'] = False
        return JsonResponse(dic)
    if Vehiculo.objects.filter(patentevehiculo = patentenew).exists():
         dic['val_patente'] = False
         print("patente existente")
    return JsonResponse(dic)

#Modificar
def editRepartidor(request,rutrepartidor):
    repartidor = get_object_or_404(Repartidor,rutrepartidor=rutrepartidor)
    vehiculo = get_object_or_404(Vehiculo,rutrepartidor=rutrepartidor)
    repartidores = Repartidor.objects.all()
   
    dataMod = {
       'selection' : repartidor,
       'repartidores':repartidores,
       'vehiculos': vehiculo,
       'categoria':listar_categoria()
    }
    if request.method == 'POST':
        rutrepartidor = request.POST.get('RutRepartidor')
        nombres = request.POST.get('NombresRepartido')
        apellido = request.POST.get('ApellidosRepartidor')
        fechacontrato = request.POST.get('Fechacontrato')   
        
        rutrestaurante = request.POST.get('rutempresa')
        #vehiculo
        patente= request.POST.get('Patentenew').upper()
        modelo = request.POST.get('Modelo')
        ano = request.POST.get('Ano')
        rutrepveh = request.POST.get('rutveh')
        color = request.POST.get('Color') 
        tipovehiculo = request.POST.get('tipovehiculo') 
        idvehhiculo = request.POST.get('idvehiculo') 
        modificar_vehiculo(patente , modelo, ano, color,rutrepveh,tipovehiculo,idvehhiculo)
        modificar_repartidor(rutrepartidor,nombres, apellido, fechacontrato ,rutrestaurante) 
        messages.success(request,'Modificado con exito')
        return redirect(to="/administracion/listarep")
    return render(request,"updaterepartidor.html",dataMod)

@permission_required('core')
def deleterepartidor(request,rutrepartidor):
    repartidor = get_object_or_404(Repartidor, rutrepartidor = rutrepartidor)
    vehiculo = get_object_or_404(Vehiculo, rutrepartidor = rutrepartidor)
    vehiculo.delete()
    repartidor.delete()
    messages.success(request,  ' Repartidor ' + repartidor.nombres + ' Eliminado con exito')
    return redirect(to='listarep')


#Listar
@permission_required('core')
def listarRep(request):
    global contexto
    Vehiculos = Vehiculo.objects.all()
    contexto = {
        'repartidor':listarRepartidor(),
        'vehiculo':Vehiculos
    }
    return render(request, "listadorepartidores.html", contexto)

#Procedimientos
def listar_categoria():
    django_cursor = connection.cursor() 
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    cursor.callproc("SP_LISTAR_TIPOVEHICULO", [out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def listar_restaurantes():
    django_cursor = connection.cursor() 
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    cursor.callproc("SP_LISTAR_RESTAURANTE", [out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def agregar_repartidor(RUTREPARTIDOR, NOMBRES, APELLIDOS, FECHACONTRATO, RUTRESTAURANTE):
     django_cursor = connection.cursor()
     cursor = django_cursor.connection.cursor()  
     salida = cursor.var(cx_Oracle.NUMBER)  
     cursor.callproc('SP_AGREGAR_REPARTIDOR', [RUTREPARTIDOR,NOMBRES,APELLIDOS,FECHACONTRATO,RUTRESTAURANTE, salida])
     return salida.getvalue()       

def modificar_repartidor(RUTREPARTIDOR,NOMBRES, APELLIDOS, FECHACONTRATO,RUTRESTAURANTE):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_MODIFICAR_REPARTIDOR',[RUTREPARTIDOR, NOMBRES, APELLIDOS, FECHACONTRATO, RUTRESTAURANTE,salida])
    return salida.getvalue()

def modificar_vehiculo(PATENTE,MODELO, ANIO, COLOR,RUTREPARTIDOR,IDTIPOVEHICULO,IDVEHICULO):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_MODIFICAR_VEHICULO',[PATENTE, MODELO, ANIO, COLOR,RUTREPARTIDOR,IDTIPOVEHICULO,IDVEHICULO,salida])
    return salida.getvalue()

def agregar_vehiculo(PATENTEVEHICULO, MODELO, ANIO, COLOR, RUTREPARTIDOR,IDVEHICULO):
     django_cursor = connection.cursor()    
     cursor = django_cursor.connection.cursor()   
     salidavhe = cursor.var(cx_Oracle.NUMBER)    
     cursor.callproc('SP_AGREGAR_VEHICULO',[PATENTEVEHICULO,MODELO,ANIO,COLOR,RUTREPARTIDOR, IDVEHICULO,salidavhe])
     return salidavhe.getvalue()        

def listarRepartidor():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_REPARTIDORES", [out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

@permission_required('core')
def repartidorRut(request):
    global contexto
    if request.method == 'POST':

        rut = request.POST.get('repartidorRut')

        Vehiculos = Vehiculo.objects.all()
        contexto = {
        'repartidor':listarRepartidorRut(rut),
        'vehiculo':Vehiculos
    }
    return render(request, 'listadorepartidores.html', contexto)


def listarRepartidorRut(rut):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_REPARTIDORES_RUT", [rut, out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista