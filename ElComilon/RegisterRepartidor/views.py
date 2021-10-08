from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
import cx_Oracle
from core.models import *

def registroVeh(request):
    print(listar_categoria())
    data = {
          'categoria':listar_categoria()
          }
    if  request.method == 'POST':
        vehiculo = Vehiculo()
        rutrepartidor = request.POST.get('RutRepartidor')
        patente = request.POST.get('Patente')
        modelo = request.POST.get('Modelo')
        ano = request.POST.get('Ano')
        color = request.POST.get('Color') 
        tipovehiculo = request.POST.get('tipovehiculo') 
        vehiculo.patentevehiculo = patente
        vehiculo.modelo = modelo
        vehiculo.anio = ano
        vehiculo.color = color
        tipovehiculo = request.POST.get('tipovehiculo') 
        try:
            Repartidorvehiculo = Repartidor.objects.get(rutrepartidor = rutrepartidor)
            vehiculo.rutrepartidor = Repartidorvehiculo
            idtipovehiculo = TipoVehiculo.objects.get(idtipovehiculo = tipovehiculo)
            vehiculo.idtipovehiculo = idtipovehiculo
            if vehiculo.save():
                print("Exito al ingresa el vehiculo")
                render(request, 'index.html')
            else:
                print("Error")
        except:
            print("Fallo")  
    return render(request, 'Registrorepartidor.html', data)  


def registroRep(request):
    print(listar_categoria())
    data = {
          'categoria':listar_categoria()
          }
    
    if request.method == 'POST':
        repartidor = Repartidor()
        rutrepartidor = request.POST.get('RutRepartidor')
        nombres = request.POST.get('NombresRepartido')
        apellido = request.POST.get('ApellidosRepartidor')
        fechacontrato = request.POST.get('Fechacontrato')
        usuario = request.POST.get('Usuario')
        contrasena = request.POST.get('contrasena')
        rutrestaurante = request.POST.get('rutempresa')
        #Agregar Repartidor
        repartidor.rutrepartidor = rutrepartidor
        repartidor.nombres = nombres
        repartidor.apellidos = apellido
        repartidor.fechacontrato = fechacontrato
        repartidor.usuario = usuario
        repartidor.contrasena = contrasena
        try:
            restaurante = Restaurante.objects.get(rutrestaurante = rutrestaurante )
            repartidor.rutrestaurante = restaurante
            if repartidor.save():
                print("Exito al ingresar repartidor")
                render(request, 'index.html')
            else:
                print("Error en ingresar ")
        except:
            print("Fallo")    
    return render(request, 'Registrorepartidor.html', data)  
 
def listar_categoria():
    django_cursor = connection.cursor() 
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    cursor.callproc("SP_LISTAR_TIPOVEHICULO", [out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista
# def agregar_repartidor(RUTREPARTIDOR, NOMBRES, APELLIDOS, FECHACONTRATO, USUARIO, CONTRASENA, RUTRESTAURANTE):
#      django_cursor = connection.cursor()
#      cursor = django_cursor.connection.cursor()    
#      cursor.callproc('SP_AGREGAR_REPARTIDOR', [RUTREPARTIDOR,NOMBRES,APELLIDOS,FECHACONTRATO,USUARIO,CONTRASENA,RUTRESTAURANTE, salida])
#     #  return salida.getvalue()       

# def agregar_vehiculo(PATENTEVEHICULO, MODELO, ANIO, COLOR, RUTREPARTIDOR, IDTIPOVEHICULO):
#      django_cursor = connection.cursor()
#      cursor = django_cursor.connection.cursor()   
#      salida = cursor.var(cx_Oracle)    
#      cursor.callproc('SP_AGREGAR_VEHICULO', [PATENTEVEHICULO,MODELO,ANIO,COLOR,USUARIO,RUTREPARTIDOR,IDTIPOVEHICULO, salida])
#      return salida.getvalue()        