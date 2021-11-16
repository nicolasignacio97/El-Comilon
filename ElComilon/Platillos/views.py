from django.shortcuts import redirect, render
from .context_processors import total_carrito
from django.db import connection
from Platillos.carrito import carrito
from core.models import Platillo
import base64

# Create your views here.
def platillos(request):
    data = {
        'platillos':listado_platillos()
    }
    return render(request, 'platillos.html', data)

def listado_platillos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PLATILLOS", [out_cur])    

    lista = []
    for fila in out_cur:
        data = {
            'data':fila,
            'imagen':str(base64.b64encode(fila[4].read()), 'utf-8')
        }
        lista.append(data)
    return lista

def agregar_producto(request, id):
    Carrito = carrito(request)
    producto = Platillo.objects.get( idplatillo = id)
    Carrito.agregar(producto)
    return redirect("platillos")
    
def eliminar_producto(request, id):
    Carrito = carrito(request)
    producto = Platillo.objects.get( idplatillo = id)
    Carrito.eliminiar(producto)
    return redirect("platillos")

def restar_producto(request,id):
    Carrito = carrito(request)
    producto = Platillo.objects.get( idplatillo = id)
    Carrito.restar(producto)
    return redirect("platillos")

def limpiar_carrito(request):
    Carrito = carrito(request)
    Carrito.limpiar()
    return redirect("platillos")

def guardar(request):
    
    Carrito = carrito(request)
    carro = Carrito.caja()
    
    print('id ',carro[0]['idplatillo'])
    print('Plato ',carro[0]['nombre'])
    print('ingredientes ',carro[0]['ingredientes'])
    print('valor ',carro[0]['valorunitario'])
    print('cantidad ',carro[0]['cantidad'])
    #print('completo',carro)
    print('TOTAL: ',total_carrito(request)['total_carrito']) 
    return redirect("platillos")