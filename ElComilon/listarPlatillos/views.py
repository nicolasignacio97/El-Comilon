from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.db import connection
import cx_Oracle
from django.core.paginator import Paginator
from core.models import Platillo
from django.contrib import messages
from django.contrib.auth.decorators import permission_required

# Create your views here.
data = {}
@permission_required('core')
def listarPlatillos(request):
    global data
    page = request.GET.get('page',1)
    Lista = listado_platillos()
    try:
        paginator = Paginator(Lista, 10)
        Lista = paginator.page(page)
    except :
        raise Http404

    data = {
        'entity': Lista,
        'paginator' : paginator,
    }
    return render(request, 'listarPlatillos.html', data)


def listado_platillos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PLATILLOS_ADMIN", [out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

@permission_required('core')
def eliminarPlatillo(request, id):
    platillo = get_object_or_404(Platillo, idplatillo=id)
    platillo.delete()
    messages.success(request, "Se ha eliminado correctamente el platillo "+ platillo.nombre)
    return redirect(to="/administracion/listarPlatillos")


def platilloNombre(request):
    global data
    if request.method == 'POST':

        nombre = request.POST.get('nombrePlatillo').upper()

        data = {
        'entity': listarPlatilloNombre(nombre)   
        }
    return render(request, 'listarPlatillos.html', data)


def listarPlatilloNombre(nombre):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PLATILLOS_NOMBRE", [nombre, out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista
