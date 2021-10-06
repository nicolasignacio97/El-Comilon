from django.shortcuts import render
from django.db import connection
import cx_Oracle

# Create your views here.
def pedido (request):
    data = {
    'Tipo_Servicio':listarTipoServicio()
}
    if request.method == 'POST':
        valorTotal = 5990
        fechaPedido = request.POST.get('Fecha').upper()
        direccionPedido = request.POST.get('Direccion')
        idTipoServicio = request.POST.get('tipoServicio')
        rutCliente = '19.134.956-3'
        idEstPedido = 1
        salida = registrarPedido(valorTotal, fechaPedido, direccionPedido, idTipoServicio, rutCliente, idEstPedido)
        if salida == 1:
            data['mensaje']='Se ha registrado el pedido correctamente'
        else:
            data['mensaje']='Error'

    return render(request, 'pedido.html', data)


def listarTipoServicio():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_TIPO_SERVICIO", [out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)
        
    return lista

def registrarPedido(valorTotal, fechaPedido, direccionPedido, idTipoServicio, rutCliente, idEstPedido):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("INSERTAR_PEDIDO", [valorTotal, fechaPedido, direccionPedido, idTipoServicio, rutCliente, idEstPedido, salida]) 
    return salida.getvalue()