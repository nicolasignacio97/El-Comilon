from datetime import date, datetime
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.db import connection
from core.models import Repartidor,Restaurante,TipoVehiculo
from registroDeUsuarios.forms import FormularioUsuario
from .forms import Repartidorform,vehiculoform,registerRepartidor
from django.contrib import messages
from django.contrib.auth.models import User
import cx_Oracle
from core.models import *

def pruebaform(request):
    form = registerRepartidor(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        print("que vello dia")
    return render(request, "regrepartidor.html", {'form':form})

def registroVeh(request):

    data = {
          'categoria':listar_categoria(), 
          
          }
    return render(request, 'Registrorepartidor.html', data)  
 
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
        # user = nombres[:2] + "." + apellido[0:]
        rutrestaurante = request.POST.get('rutempresa')
        
        #Vehiculo
        vehiculorut = request.POST.get('RutRepartidor')
        patente = request.POST.get('Patente')
        modelo = request.POST.get('Modelo')
        ano = request.POST.get('Ano')
        color = request.POST.get('Color') 
        tipovehiculo = request.POST.get('tipovehiculo') 
        # if not Restaurante.objects.filter(rutrestaurante = rutrestaurante).exists():
        #     print("Rut Empresa existente")
        #     messages.error(request, 'Rut restaurante no valido')
        #     #return redirect(to="/regin")
        # if Repartidor.objects.filter(rutrepartidor = rutrepartidor).exists():
        #     print("Usuario existente")
        #     messages.add_message(request, messages.INFO, 'Repartidor YA REGISTRADO .')
        #     #return redirect(to="/regin")        
        # else:
        forumulario = FormularioUsuario(data=request.POST)
        if forumulario.is_valid():
            forumulario.save()
            data['form'] = forumulario
            agregar_repartidor(rutrepartidor, nombres, apellido, fechacontrato, rutrestaurante)
            agregar_vehiculo(patente,modelo,ano,color,vehiculorut,tipovehiculo)
            messages.success(request, 'Repartidor Registrado con exito')
            return render(request, 'Registrorepartidor.html', data)        
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
    # return JsonResponse({'valid': 0})
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
    print('entrando al metodo')
    print(vehiculo.idtipovehiculo)
    print()
    
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
        # user = nombres[:2] + "." + apellido[0:]
        rutrestaurante = request.POST.get('rutempresa')
        #vehiculo
        patente= request.POST.get('Patentenew').upper()
        modelo = request.POST.get('Modelo')
        ano = request.POST.get('Ano')
        rutrepveh = request.POST.get('rutveh')
        color = request.POST.get('Color') 
        tipovehiculo = request.POST.get('tipovehiculo') 
        idvehhiculo = request.POST.get('idvehiculo') 
        print(patente)
        print(modelo)
        print(ano)
        print(color)
        print(rutrepveh)
        print(tipovehiculo)
        print(idvehhiculo)
        modificar_vehiculo(patente , modelo, ano, color,rutrepveh,tipovehiculo,idvehhiculo)
        modificar_repartidor(rutrepartidor,nombres, apellido, fechacontrato ,rutrestaurante) 
        messages.success(request,'Modificado con exitos')
        return redirect(to="/administracion/listarep")
    return render(request,"updaterepartidor.html",dataMod)
def deleterepartidor(request,rutrepartidor, id):
    u = User.objects.get(pk=id)
    u.delete()
    repartidores = Repartidor.objects.all()
    vehiculos = Vehiculo.objects.all()
    vehiculo = Vehiculo.objects.get(rutrepartidor = rutrepartidor)
    vehiculo.delete()
    repartidor = Repartidor.objects.get(rutrepartidor=rutrepartidor)
    repartidor.delete()
    messages.success(request,  ' Repartidor ' + repartidor.nombres + ' Eliminado con exito')
    contexto = {
         'repartidor':repartidores
    }
    return render(request,"listadorepartidores.html",contexto)

#Listar
def listarRep(request):
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