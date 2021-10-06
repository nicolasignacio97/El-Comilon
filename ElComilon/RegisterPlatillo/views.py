from django.shortcuts import render
from django.db import connection
import cx_Oracle

# Create your views here.
def registroPlatillo (request):
    data = {
    'Restaurante':listarRestaurante()
}
    if request.method == 'POST':
        nombrePlatillo = request.POST.get('Nombre').upper()
        ingredientes = request.POST.get('Ingredientes').upper()
        valor = request.POST.get('Valor')
        foto = request.FILES['foto'].read()
        rutRestaurante = request.POST.get('restaurante')
        salida = registrarPlatillo(nombrePlatillo, ingredientes, valor, foto, rutRestaurante)
        if salida == 1:
            data['mensaje']='Se ha registrado el platillo correctamente'
            salida = 0
        else:
            data['mensaje']='Error'
    return render(request,'registrarPlatillo.html', data)

def listarRestaurante():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_RESTAURANT", [out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def registrarPlatillo(nomPlatillo, ingPlatillo, valPlatillo, fotPlatillo, rutRest):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("INSERTAR_PLATILLO", [nomPlatillo, ingPlatillo, valPlatillo, fotPlatillo, rutRest, salida]) 
    return salida.getvalue()