from django.shortcuts import render,redirect
from django.db import connection
from core.models import Repartidor,Restaurante
from registroDeUsuarios.forms import FormularioUsuario
from .forms import Repartidorform,vehiculoform,registerRepartidor
from django.contrib import messages
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
        if not Restaurante.objects.filter(rutrestaurante = rutrestaurante).exists():
            print("Rut Empresa existente")
            messages.success(request, 'Rut restaurante no valido')
            #return redirect(to="/regin")
        if Repartidor.objects.filter(rutrepartidor = rutrepartidor).exists():
            print("Usuario existente")
            messages.success(request, 'Repartidor ya existente')
            #return redirect(to="/regin")        
        else:
            forumulario = FormularioUsuario(data=request.POST)
            if forumulario.is_valid():
                forumulario.save()
                data['form'] = forumulario
                agregar_repartidor(rutrepartidor, nombres, apellido, fechacontrato, rutrestaurante)
                agregar_vehiculo(patente,modelo,ano,color,vehiculorut,tipovehiculo)
                messages.success(request, 'Repartidor Registrado con exito')
                return render(request, 'Registrorepartidor.html', data)        

        
    return render(request, 'Registrorepartidor.html', data)  


def editRepartidor(request,rutrepartidor):
    repartidor = Repartidor.objects.get(rutrepartidor=rutrepartidor)
    repartidores = Repartidor.objects.all()
    if request.method == 'GET':
        form = Repartidorform(instance=repartidor)
        contexto = {
            'form':form
        }
        
    else: 
        form = Repartidorform(request.POST, instance=repartidor)
        contexto = {
            'form':form,
            'repartidor':repartidores
        }
        if form.is_valid():
           form.save()
           messages.success(request, 'Repartidor editado con exito') 
           return render(request, "listadorepartidores.html", contexto)
           redirect( to = "listarep")
    return render(request, "updaterepartidor.html",contexto)

def editvehiculo(request,rutrepartidor):
     vehiculo = Vehiculo.objects.get(rutrepartidor=rutrepartidor)
     Vehiculos =  Vehiculo.objects.all()
     if request.method == 'GET':
        form = vehiculoform(instance=vehiculo)
        contexto = {
            'form':form
        }
     else: 
        form = vehiculoform(request.POST, instance=vehiculo)
        contexto = {
            'vehiculo':Vehiculos
        }
        if form.is_valid():
           form.save() 
        messages.success(request, 'Editado con exito')
        return redirect(to="/administracion/listarep")
     return render(request, "updatevehiculo.html",contexto)


def deleterepartidor(request,rutrepartidor):
    repartidores = Repartidor.objects.all()
    vehiculos = Vehiculo.objects.all()
    vehiculo = Vehiculo.objects.get(rutrepartidor = rutrepartidor)
    vehiculo.delete()
    repartidor = Repartidor.objects.get(rutrepartidor=rutrepartidor)
    repartidor.delete()
    messages.success(request, messages.SUCCESS , 'Eliminado con exito')
    contexto = {
         'repartidor':repartidores
    }
    return render(request,"listadorepartidores.html",contexto)


def listarRep(request):
    repartidores = Repartidor.objects.all()
    Vehiculos = Vehiculo.objects.all()
    contexto = {
        'repartidor':repartidores,
        'vehiculo':Vehiculos
    }
    return render(request, "listadorepartidores.html", contexto)

def listar_categoria():
    django_cursor = connection.cursor() 
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    cursor.callproc("SP_LISTAR_TIPOVEHICULO", [out_cur])
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

def agregar_vehiculo(PATENTEVEHICULO, MODELO, ANIO, COLOR, RUTREPARTIDOR, IDTIPOVEHICULO):
     django_cursor = connection.cursor()    
     cursor = django_cursor.connection.cursor()   
     salidavhe = cursor.var(cx_Oracle.NUMBER)    
     cursor.callproc('SP_AGREGAR_VEHICULO',[PATENTEVEHICULO,MODELO,ANIO,COLOR,RUTREPARTIDOR,IDTIPOVEHICULO, salidavhe])
     return salidavhe.getvalue()        